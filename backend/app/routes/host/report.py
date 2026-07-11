from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from backend.app.services.host_report import build_report_data

report_bp = Blueprint("report", __name__, url_prefix="/reports")


@report_bp.route("/")
@login_required
def index():
    period = request.args.get("period", "30d")
    if period not in ("7d", "30d", "year", "all"):
        period = "30d"
    acc_id = request.args.get("acc_id", type=int)
    page = request.args.get("page", 1, type=int)

    data = build_report_data(current_user.id, period, acc_id)
    per_page = 10
    txs = data["transactions"]
    total = len(txs)
    start = (page - 1) * per_page
    end = start + per_page
    data["transactions_page"] = txs[start:end]
    data["pagination"] = {
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": max(1, (total + per_page - 1) // per_page),
        "start": start + 1 if total else 0,
        "end": min(end, total),
    }

    return render_template("host/report/index.html", active_nav="reports", **data)


@report_bp.route("/export/<fmt>")
@login_required
def export(fmt):
    period = request.args.get("period", "30d")
    acc_id = request.args.get("acc_id", type=int)
    data = build_report_data(current_user.id, period, acc_id)
    if fmt == "csv":
        import csv
        import io
        from flask import Response

        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["Ngày", "CSLT", "Phòng", "Mã booking", "Doanh thu", "Trạng thái"])
        for t in data["transactions"]:
            writer.writerow([t["date"], t["acc"], t["room"], t["code"], t["revenue"], t["status"]])
        return Response(
            buf.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=bao-cao-rova.csv"},
        )
    return redirect(url_for("report.index", period=period, acc_id=acc_id or None))
