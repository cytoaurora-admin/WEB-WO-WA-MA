from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Max
from django.db.models.functions import Substr, Length
from django.utils import timezone
from datetime import datetime, timedelta
from .filters import *
from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admin_only
import logging


@login_required(login_url="login")
def add_patient(request):
    logger = logging.getLogger(__name__)

    if request.method == "POST":
        cat_id = request.POST["cat_id"]
        patient_name = request.POST["patient_name"]
        birthday = request.POST["birthday"]
        initial_diagnosis = request.POST["initial_diagnosis"]
        gender = request.POST["gender"]
        record_number = request.POST["record_number"]
        comment = request.POST["comment"]
        hospital = request.POST["source"]

        # 加密病人姓名
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT '\\x' || encode(public.encrypt_info(convert_to(%s, 'UTF8')), 'hex')",
                [patient_name],
            )
            encrypted_patient_name = cursor.fetchone()[0]

        patient = Patient.objects.create(
            cat_id=cat_id,
            patient_name=encrypted_patient_name,
            birthday=birthday,
            initial_diagnosis=initial_diagnosis,
            gender=gender,
            record_number=record_number,
            comment=comment,
            hospital=hospital,
        )

        messages.success(request, "添加成功！病人的医华病历编码为：" + cat_id)
        logger.info(
            'Patient "%s" is created',
            cat_id,
            extra={"user": request.user.username, "cat_id": cat_id},
        )

        return redirect("add_patient")
    else:
        # 查詢資料庫以獲取最新的病歷編碼
        last_patient = Patient.objects.order_by("-id").first()
        last_cat_id = last_patient.cat_id if last_patient else None
        if last_cat_id:
            last_number = int(last_cat_id[3:])  # 獲取最後一個病人的數字部分
        else:
            last_number = 0
        new_number = last_number + 1
        next_cat_id = (
            f"PMS{new_number:05}"  # 將數字部分格式化為5位數，不足的部分用0補齊
        )

    # 取得單位資料表
    sources = SourceDropdown.objects.filter(visible=1)

    context = {"next_cat_id": next_cat_id, "sources": sources}
    return render(request, "WO/add_patient.html", context)


def decrypt_patient_name(patient):
    # 解密病人姓名
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT public.decrypt_info(decode(substring(%s from 3), 'hex'))",
            [patient.patient_name],
        )
        decrypted_patient_name = cursor.fetchone()[0]

    if len(decrypted_patient_name) > 1:
        patient.patient_name = (
            decrypted_patient_name[:1] + "@" + decrypted_patient_name[2:]
        )

    return patient


def query_patient(query_param):
    if query_param:
        patients = Patient.objects.all()
        patient_filter = PatientFilter({"fuzzy_query": query_param}, queryset=patients)
        filtered_patients = patient_filter.qs

        for patient in filtered_patients:
            patient = decrypt_patient_name(patient)
    else:
        filtered_patients = Patient.objects.none()

    return filtered_patients


@login_required(login_url="login")
def create_sample_barcode(request):
    logger = logging.getLogger(__name__)

    # 查詢病人紀錄
    query_param = request.GET.get("fuzzy_query", "").strip()  # 獲取並去除输入的空格
    filtered_patients = query_patient(query_param)

    # 取得項目資料表
    projects = ProjectDropdown.objects.filter(visible=1)

    # 取得單位資料表
    sources = SourceDropdown.objects.filter(visible=1)

    # 取得project的最大檢體編碼
    selected_project = request.POST.get("project")
    sample_barcode_project_num = SampleBarcode.objects.filter(project=selected_project)
    max_barcode = sample_barcode_project_num.aggregate(Max("sample_barcode"))[
        "sample_barcode__max"
    ]
    if max_barcode is not None:
        number = int(max_barcode[6:9]) + 1
        if number > 999:
            number = "!!"
        else:
            # 將數字格式化為三位數的字串
            number = str(number).zfill(3)
    else:
        number = "001"
    if number == "999":
        number = "!!"

    # 處理檢體資料
    if request.method == "POST":
        project = request.POST.get("project")
        source = request.POST.get("source")
        extract = request.POST.get("extract")
        cat_id = request.POST.get("cat_id_temp")
        physical_comment = request.POST.get("physical_comment")
        histological_comment = request.POST.get("histological_comment")
        nub_tube = request.POST.get("nub_tube")
        sample_quality = request.POST.get("sample_quality")
        existing_sample_barcode = request.POST.get("existing_sample_barcode")

        # 生成檢體編碼
        for i in range(1, int(nub_tube) + 1):
            tube_type = request.POST.get(f"tube_type{str(i)}")

            patient = Patient.objects.get(
                cat_id=cat_id
            )  # 使用 cat_id 獲取 Patient 實例

            date = timezone.now()
            year_ascii = chr(date.year - 1951)
            week_of_year = date.strftime("%W")
            day_of_week = date.weekday()

            sample_barcode = (
                f"{project}{year_ascii}{week_of_year.zfill(2)}{day_of_week}{number}"
            )
            sample_barcode_detail = sample_barcode + "-" + str(i) + "-"

            sample = SampleBarcode.objects.create(
                sample_barcode_detail=sample_barcode_detail,
                sample_barcode=sample_barcode,
                project=project,
                source=source,
                extract=extract,
                cat=patient,
                physical_comment=physical_comment,
                histological_comment=histological_comment,
                tube_type=tube_type,
                sample_quality=sample_quality,
                existing_sample_barcode=existing_sample_barcode,
                quota=30,
                done=0,
                expired=0,
                lock=0,
            )

            logger.info(
                'Sample barcode detail "%s" is created',
                sample_barcode_detail,
                extra={
                    "user": request.user.username,
                    "sample_barcode_detail": sample_barcode_detail,
                },
            )

        messages.success(request, "产生并储存检体编码成功！" + sample_barcode)

        context = {"sample_barcode": sample_barcode}
        return render(request, "WO/create_sample_barcode.html", context)

    context = {
        "filtered_patients": filtered_patients,
        "projects": projects,
        "sources": sources,
        "number": number,
    }
    return render(request, "WO/create_sample_barcode.html", context)


@login_required(login_url="login")
def create_qrcode_wo(request):
    logger = logging.getLogger(__name__)

    # 取得需要的選單資料
    locations = LocationDropdown.objects.filter(visible=1)
    sample_barcodes = SampleBarcode.objects.filter(expired=0)
    patients = Patient.objects.all()
    antibody_types = AntibodyDropdown.objects.filter(visible=1)
    chip_types = ChipDropdown.objects.filter(visible=1)
    cover_types = CoverDropdown.objects.filter(visible=1)
    operating_types = OperatingDropdown.objects.filter(visible=1)
    preprocess_types = PreprocessDropdown.objects.filter(visible=1)

    if request.method == "POST":
        selected_location = request.POST.get("location")
        selected_sn = request.POST.get("serial_number")
        wo_comment = request.POST.get("wo_comment")
        work_order_type = request.POST.get("work_order_type")
        ver = "c"
        add_time = timezone.now().replace(microsecond=0)
        wo_owner = request.POST.get("wo_owner")
        detection_code = request.POST.get("detection_code")

        try:
            causer_instance = CaUser.objects.get(userid=wo_owner)
        except CaUser.DoesNotExist:
            messages.error(request, "找不到该工单负责人！")
            pass

        # 獲取檢驗時間
        date_string = request.POST.get("date")
        date = datetime.strptime(date_string, "%Y-%m-%d")  # 將日期字串轉換為日期物件
        year_ascii = chr(date.year - 1951)
        date_month = date.strftime("%m")
        date_day = date.strftime("%d")

        # 獲取工單編碼
        query_wo = Qrcode.objects.filter(
            location=selected_location, date=date, version="c"
        )
        query_wo = (
            query_wo.annotate(index=Substr("work_order", Length("work_order")))
            .order_by("-index")
            .first()
        )

        if query_wo is None:
            work_order_index = "1"
        else:
            index = query_wo.index
            if index == "9":
                work_order_index = "A"
            elif index == "Z":
                work_order_index = "0"
            else:
                if index.isdigit():
                    work_order_index = str(int(index) + 1)
                else:
                    work_order_index = chr(ord(index) + 1)

        # 生成工單編碼
        work_order = f"{selected_location}{year_ascii}{date_month}{date_day}{work_order_type}{work_order_index}"

        work_order_record = WorkOrder.objects.create(
            work_order=work_order,
            add_time=add_time,
            comment=wo_comment,
            owner=causer_instance,
        )

        logger.info(
            'Work order "%s" is created by %s',
            work_order,
            causer_instance.userid,
            extra={
                "user": request.user.username,
                "work_order": work_order,
                "owner": causer_instance.userid,
            },
        )

        selected_antibody_types = [
            "A" + detection_code[i : i + 2] for i in range(0, len(detection_code), 2)
        ]
        index = 0

        for i, selected_antibody_type in enumerate(selected_antibody_types, start=1):
            for j in range(1, int(selected_sn) + 1):
                index += 1

                machine = request.POST.get(f"machine{str(index)}")
                comment = request.POST.get(f"comment{str(index)}")

                """ 
                執行SQL查詢從qrcode表中選擇work_order
                其中location、version和date與POST請求中的值匹配
                按照work_order降序排序並只返回第一個結果
                """

                # 獲取檢體編碼
                selected_sample_barcode_detail = request.POST.get("sample_barcode")
                sample_barcode_detail = SampleBarcode.objects.get(
                    sample_barcode_detail=selected_sample_barcode_detail
                )
                sample_barcode = sample_barcode_detail.sample_barcode

                # 生成兩種編碼
                experiment_barcode = f"{selected_antibody_type}.---.---.---.--{j}"
                qrcode = f"{sample_barcode}_{experiment_barcode}_{work_order}{ver}"

                if Qrcode.objects.filter(qrcode=qrcode).exists():
                    continue

                record = Qrcode.objects.create(
                    qrcode=qrcode,
                    sample_barcode_detail=sample_barcode_detail,
                    experiment_barcode=experiment_barcode,
                    location=selected_location,
                    date=date,
                    version=ver,
                    antibody_type=selected_antibody_type,
                    chip_type="---",
                    cover_type="---",
                    operating_type="---",
                    preprocess_type="--",
                    comment=comment,
                    work_order=work_order_record,  # 將 WorkOrder 實例賦值給 Qrcode.work_order
                    machine=machine,
                )

                logger.info(
                    'Qrcode "%s" is created',
                    qrcode,
                    extra={"user": request.user.username, "qrcode": qrcode},
                )

                sample_barcode_detail.done += 1
                sample_barcode_detail.save()

        messages.success(request, "已产生检体编码及工单！" + work_order)

    context = {
        "locations": locations,
        "sample_barcodes": sample_barcodes,
        "patients": patients,
        "antibody_types": antibody_types,
        "chip_types": chip_types,
        "cover_types": cover_types,
        "operating_types": operating_types,
        "preprocess_types": preprocess_types,
    }
    return render(request, "WO/create_qrcode_wo.html", context)


@login_required(login_url="login")
def wo_export(request):
    logger = logging.getLogger(__name__)

    # 獲取地點資料表
    locations = LocationDropdown.objects.filter(visible=1)

    work_orders = WorkOrder.objects.all()

    # 使用 ReceiveTimeFilter 進行第一次過濾
    receive_time_filter = ReceiveTimeFilter(
        {"receive_time_null": False}, queryset=work_orders
    )
    filtered_wo_list = receive_time_filter.qs

    # 然後使用 WorkOrderFilter 進行第二次過濾
    if request.GET and (request.GET.get("date") or request.GET.get("location")):
        wo_filter = WorkOrderFilter(request.GET, queryset=filtered_wo_list)
    else:
        wo_filter = WorkOrderFilter(queryset=Qrcode.objects.none())
    filtered_wo_list = wo_filter.qs.distinct("work_order")

    # 接收工單
    if request.method == "POST":
        wo_result = request.POST.get("wo_result")
        work_order = get_object_or_404(WorkOrder, work_order=wo_result)
        work_order.receive_time = timezone.now().replace(microsecond=0)
        work_order.deadline = timezone.now().replace(microsecond=0) + timedelta(
            hours=168
        )
        work_order.wo_export = wo_result  # 將 wo_result 的值賦給 wo_export

        work_order.save()
        messages.success(request, "成功接收工单！" + wo_result)
        logger.info(
            'Work order "%s" is received',
            work_order.work_order,
            extra={"user": request.user.username, "work_order": work_order.work_order},
        )
    else:
        wo_result = None

    # 預覽工單
    if request.GET.get("wo_export"):
        wo_export = request.GET.get("wo_export", "").strip()
        selected_qrs = Qrcode.objects.filter(work_order=wo_export).order_by("qrcode")
        selected_wo = WorkOrder.objects.get(work_order=wo_export)
        description = selected_wo.comment
        receive_time = selected_wo.receive_time
        deadline = selected_wo.deadline

        # 處理多筆 Qrcode 資料
        for qr in selected_qrs:
            location_dropdown = LocationDropdown.objects.get(option_value=qr.location)
            location = location_dropdown.option_text
            date = qr.date
            qrcode = qr.qrcode
            sample_barcode_detail = qr.sample_barcode_detail
            work_order = qr.work_order
            machine = qr.machine
            antibody_type = qr.antibody_type
            chip_type = qr.chip_type
            cover_type = qr.cover_type
            comment = qr.comment
    else:
        location = None
        date = None
        qrcode = None
        sample_barcode_detail = None
        work_order = None
        description = None
        receive_time = None
        deadline = None
        selected_qrs = None
        machine = None
        antibody_type = None
        chip_type = None
        cover_type = None
        comment = None

    context = {
        "locations": locations,
        "filtered_wo_list": filtered_wo_list,
        "wo_result": wo_result,
        "date": date,
        "qrcode": qrcode,
        "sample_barcode_detail": sample_barcode_detail,
        "location": location,
        "work_order": work_order,
        "description": description,
        "receive_time": receive_time,
        "deadline": deadline,
        "selected_qrs": selected_qrs,
        "machine": machine,
        "antibody": antibody_type,
        "chip": chip_type,
        "cover": cover_type,
        "comment": comment,
    }
    return render(request, "WO/wo_export.html", context)


@login_required(login_url="login")
def query_qrcode(request):
    query_param = request.GET.get("fuzzy_query", "").strip()
    filtered_patients = query_patient(query_param)

    for patient in filtered_patients:
        qrcodes = Qrcode.objects.filter(sample_barcode_detail__cat_id=patient.cat_id)
        patient.qrcodes_comments = [
            (qrcode, qrcode.sample_barcode_detail.histological_comment)
            for qrcode in qrcodes
        ]

    context = {"filtered_patients": filtered_patients}
    return render(request, "WO/query_qrcode.html", context)


@login_required(login_url="login")
def query_sample_barcode(request):
    sample_barcodes = SampleBarcode.objects.none()

    if request.method == "GET":
        date1_str = request.GET.get("date1")
        date2_str = request.GET.get("date2")

        if date1_str and date2_str:
            date1 = datetime.strptime(date1_str, "%Y-%m-%d").date()
            date2 = datetime.strptime(date2_str, "%Y-%m-%d").date()

            # 使用 select_related 獲取相關的 Patient 對象
            sample_barcodes = (
                SampleBarcode.objects.select_related("cat").all().order_by("extract")
            )

            filter = QuerySampleBarcodeFilter(
                {"extract_after": date1, "extract_before": date2},
                queryset=sample_barcodes,
            )
            sample_barcodes = filter.qs

            for sample_barcode in sample_barcodes:
                sample_barcode.cat = decrypt_patient_name(sample_barcode.cat)

    context = {"sample_barcodes": sample_barcodes}
    return render(request, "WO/query_sample_barcode.html", context)


@login_required(login_url="login")
def recycle_qrcode(request):
    logger = logging.getLogger(__name__)

    if request.method == "POST":
        qrcode = request.POST.get("qrcode", "").strip()
        print(f"QR code from DB: {qrcode}")
        if qrcode:
            try:
                qrcode_entry = Qrcode.objects.get(qrcode=qrcode)
                print("Found QR code in database, deleting...")
                qrcode_entry.delete()
                messages.success(request, "成功回收 QR 码！")
                logger.info(
                    'Qrcode "%s" is recycled',
                    qrcode,
                    extra={"user": request.user.username, "qrcode": qrcode},
                )
            except Qrcode.DoesNotExist:
                print("QR code not found in database")
                messages.error(request, "找不到该 QR 码！")
    context = {}
    return render(request, "WO/recycle_qrcode.html", context)


@login_required(login_url="login")
def update_wo_finish_time(request):
    logger = logging.getLogger(__name__)

    if request.method == "POST":
        work_order = request.POST.get("work_order")
        finish_date = request.POST.get("finish_date")

        finish_date = datetime.strptime(finish_date, "%Y-%m-%dT%H:%M")

        wo = WorkOrder.objects.get(work_order=work_order)
        wo.finish_time = finish_date
        wo.save()

        messages.success(request, "工单完成时间已更新！")
        logger.info(
            'WO "%s" is recycled',
            work_order,
            extra={"user": request.user.username, "work_order": work_order},
        )

    context = {}
    return render(request, "WO/update_wo_finish_time.html", context)


@login_required(login_url="login")
def update_qrcode(request):
    if request.method == "GET":
        qrcode_value = request.GET.get("qrcode", "").strip()

        antibody_types = AntibodyDropdown.objects.filter(visible=1)
        chip_types = ChipDropdown.objects.filter(visible=1)
        cover_types = CoverDropdown.objects.filter(visible=1)
        operating_types = OperatingDropdown.objects.filter(visible=1)
        preprocess_types = PreprocessDropdown.objects.filter(visible=1)
        machines = Machine.objects.filter(location_value="G", visible=1)

        if qrcode_value:
            if len(qrcode_value) != 39:
                messages.error(request, "错误的QR码格式")
                return redirect("update_qrcode")
            try:
                qrcode = get_object_or_404(Qrcode, pk=qrcode_value)
                print(f"qrcode.machine: {qrcode.machine}")

                try:
                    sample_barcode = SampleBarcode.objects.get(qrcode=qrcode_value)
                    project = sample_barcode.project
                    source = sample_barcode.source
                    extract = sample_barcode.extract

                    patient = Patient.objects.get(cat_id=sample_barcode.cat.cat_id)
                    cat_id = patient.cat_id
                    record_number = patient.record_number

                except SampleBarcode.DoesNotExist:
                    return redirect("update_qrcode")
                except Patient.DoesNotExist:
                    return redirect("update_qrcode")

                context = {
                    "antibody_type": qrcode.antibody_type,
                    "cover_type": qrcode.cover_type,
                    "chip_type": qrcode.chip_type,
                    "operating_type": qrcode.operating_type,
                    "preprocess_type": qrcode.preprocess_type,
                    "comment": qrcode.comment,
                    "machine": qrcode.machine,
                    "location": qrcode.location,
                    "date": qrcode.date,
                    "project": project,
                    "source": source,
                    "extract": extract,
                    "cat_id": cat_id,
                    "record_number": record_number,
                    "antibody_types": antibody_types,
                    "chip_types": chip_types,
                    "cover_types": cover_types,
                    "operating_types": operating_types,
                    "preprocess_types": preprocess_types,
                    "machines": machines,
                }
            except:
                messages.error(request, "找不到该笔资料")
                return redirect("update_qrcode")
        else:
            context = {
                "antibody_types": antibody_types,
                "chip_types": chip_types,
                "cover_types": cover_types,
                "operating_types": operating_types,
                "preprocess_types": preprocess_types,
                "machines": machines,
            }
        return render(request, "WO/update_qrcode.html", context)

    context = {}
    return render(request, "WO/update_qrcode.html", context)


@login_required(login_url="login")
def save_qrcode(request):
    logger = logging.getLogger(__name__)

    if request.method == "POST":
        qrcode = request.POST.get("qrcode", "").strip()
        antibody_type = request.POST.get("antibody_type")
        chip_type = request.POST.get("chip_type")
        cover_type = request.POST.get("cover_type")
        operating_type = request.POST.get("operating_type")
        preprocess_type = request.POST.get("preprocess_type")
        comment = request.POST.get("comment")
        machine = request.POST.get("machine")
        record_number = request.POST.get("record_number")

        try:
            qrcode_entry = Qrcode.objects.get(qrcode=qrcode)
        except Qrcode.DoesNotExist:
            messages.error(request, "找不到对应的 Qrcode！")
            return redirect("update_qrcode")

        last_digit = qrcode_entry.experiment_barcode[-1]
        new_string = f"{antibody_type}.{chip_type}.{cover_type}.{operating_type}.{preprocess_type}{last_digit}"
        qrcode_entry.experiment_barcode = new_string
        qrcode_entry.save()

        parts = qrcode_entry.qrcode.split("_")
        first_part = parts[0]
        second_part = parts[2]
        new_qrcode = f"{first_part}_{new_string}_{second_part}"

        # 假設 old_qrcode 是原本的 QRCode 的 qrcode
        old_qrcode = qrcode_entry.qrcode
        # 更新 qrcode
        qrcode_entry.qrcode = new_qrcode
        qrcode_entry.save()

        qrcode_entry.antibody_type = antibody_type
        qrcode_entry.chip_type = chip_type
        qrcode_entry.cover_type = cover_type
        qrcode_entry.operating_type = operating_type
        qrcode_entry.preprocess_type = preprocess_type
        qrcode_entry.comment = comment
        qrcode_entry.machine = machine
        qrcode_entry.save()

        sample_barcode = SampleBarcode.objects.get(qrcode=qrcode)
        patient = Patient.objects.get(cat_id=sample_barcode.cat.cat_id)
        patient.record_number = record_number
        patient.save()

        old_qrcode_entry = Qrcode.objects.get(qrcode=old_qrcode)
        if new_qrcode != old_qrcode:
            old_qrcode_entry.delete()
            messages.success(request, f"更新成功！QR码为：{new_qrcode}")
            logger.info(
                'Qrcode "%s" is updated to "%s"',
                old_qrcode,
                new_qrcode,
                extra={
                    "user": request.user.username,
                    "old_qrcode": old_qrcode,
                    "new_qrcode": new_qrcode,
                },
            )
        else:
            messages.error(request, f"更新部分资料成功！QR码为：{new_qrcode}")
            logger.info(
                'Qrcode "%s" is updated',
                new_qrcode,
                extra={"user": request.user.username, "qrcode": new_qrcode},
            )

        return redirect("update_qrcode")

    context = {}
    return render(request, "WO/update_qrcode.html", context)


@login_required(login_url="login")
def report_export(request):
    sample_barcodes = SampleBarcode.objects.none()

    if request.method == "GET":
        date1_str = request.GET.get("date1")
        date2_str = request.GET.get("date2")

        if date1_str and date2_str:
            date1 = datetime.strptime(date1_str, "%Y-%m-%d").date()
            date2 = datetime.strptime(date2_str, "%Y-%m-%d").date()

            # 使用 select_related 獲取相關的 Patient 對象
            sample_barcodes = (
                SampleBarcode.objects.select_related("cat").all().order_by("extract")
            )

            filter = QuerySampleBarcodeFilter(
                {"extract_after": date1, "extract_before": date2},
                queryset=sample_barcodes,
            )
            sample_barcodes = filter.qs

            current_year = datetime.now().year
            for sample_barcode in sample_barcodes:
                sample_barcode.cat.age = current_year - sample_barcode.cat.birthday.year
                sample_barcode.cat = decrypt_patient_name(sample_barcode.cat)
                sample_barcode.qrcodes = (
                    sample_barcode.qrcode_set.all()
                )  # Access related Qrcode objects

    context = {
        "sample_barcodes": sample_barcodes,
        "date1": date1_str,
        "date2": date2_str,
    }
    return render(request, "WO/report_export.html", context)


@login_required(login_url="login")
def update_option(request):

    context = {}
    return render(request, "WO/update_option.html", context)


@unauthenticated_user
def registerPage(request):
    logger = logging.getLogger(__name__)

    form = CreationUserForm()
    if request.method == "POST":
        form = CreationUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            group = Group.objects.get(name="user1")
            user.groups.add(group)

            messages.success(request, "添加帐号 " + username + " 成功")
            logger.info("User %s is created", user, extra={"user": user})

            return redirect("login")

    context = {"form": form}
    return render(request, "WO/register.html", context)


@unauthenticated_user
def loginPage(request):
    logger = logging.getLogger(__name__)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            logger.info(
                "User %s has logged in", request.user, extra={"user": request.user}
            )
            return redirect("add_patient")
        else:
            messages.info(request, "使用者名称或密码错误")

    context = {}
    return render(request, "WO/login.html", context)


def logoutUser(request):
    logger = logging.getLogger(__name__)
    logger.info("User %s has logged out", request.user, extra={"user": request.user})

    logout(request)
    return redirect("login")
