import csv, io
from datetime import datetime, date
from flask import render_template, request, redirect, url_for, flash, Response, send_file
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from . import db, login_manager
from .models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def register_routes(app):
    @app.context_processor
    def globals():
        return {
            "current_year": datetime.utcnow().year,
            "asset_count": Asset.query.count(),
            "request_count": ServiceRequest.query.count(),
            "open_request_count": ServiceRequest.query.filter(ServiceRequest.status.notin_(["Completed", "Closed"])) .count(),
            "vendor_count": Vendor.query.count(),
        }

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            u = User.query.filter_by(email=request.form.get("email", "").strip().lower()).first()
            if u and u.check_password(request.form.get("password", "")):
                login_user(u)
                return redirect(url_for("dashboard"))
            flash("Invalid email or password.", "danger")
        return render_template("index.html", open_auth="login")

    @app.route("/signup", methods=["GET", "POST"])
    @app.route("/register", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            if not name or not email or not password:
                flash("Name, email and password are required.", "danger")
            elif User.query.filter_by(email=email).first():
                flash("An account with that email already exists.", "warning")
            else:
                u = User(full_name=name, email=email)
                u.set_password(password)
                db.session.add(u)
                db.session.commit()
                login_user(u)
                return redirect(url_for("dashboard"))
        return render_template("index.html", open_auth="signup")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("home"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template(
            "dashboard.html",
            assets=Asset.query.order_by(Asset.id.desc()).limit(8).all(),
            requests=ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).limit(8).all(),
            predictions=FailurePrediction.query.order_by(FailurePrediction.probability.desc()).limit(5).all(),
        )

    @app.route("/assets", methods=["GET", "POST"])
    @login_required
    def asset_register():
        if request.method == "POST":
            a = Asset(
                asset_tag=request.form.get("asset_tag", ""),
                name=request.form.get("name", ""),
                category=request.form.get("category"),
                status=request.form.get("status", "Operational"),
                region=request.form.get("region"),
                site=request.form.get("site"),
                supplier=request.form.get("supplier"),
                manufacturer=request.form.get("manufacturer"),
                model=request.form.get("model"),
                criticality=request.form.get("criticality", "Medium"),
                purchase_cost=request.form.get("purchase_cost") or 0,
                current_value=request.form.get("current_value") or 0,
                expected_life_years=request.form.get("expected_life_years") or 10,
                mileage=request.form.get("mileage") or 0,
                latitude=request.form.get("latitude") or None,
                longitude=request.form.get("longitude") or None,
            )
            if not a.asset_tag or not a.name:
                flash("Asset tag and name are required.", "danger")
            elif Asset.query.filter_by(asset_tag=a.asset_tag).first():
                flash("Asset tag already exists.", "warning")
            else:
                db.session.add(a)
                db.session.commit()
                flash("Asset registered successfully.", "success")
                return redirect(url_for("asset_register"))
        q = request.args.get("q", "").strip()
        query = Asset.query
        for field in ["status", "category", "region", "site", "supplier"]:
            if request.args.get(field):
                query = query.filter(getattr(Asset, field) == request.args.get(field))
        if q:
            query = query.filter(or_(Asset.asset_tag.like(f"%{q}%"), Asset.name.like(f"%{q}%"), Asset.manufacturer.like(f"%{q}%")))
        return render_template("1.html", assets=query.order_by(Asset.id.desc()).all(), locations=Location.query.all(), vendors=Vendor.query.all())

    @app.route("/assets/register", methods=["GET", "POST"])
    @login_required
    def detailed_asset_register():
        return redirect(url_for("asset_register"))

    @app.route("/assets/<int:asset_id>")
    @login_required
    def asset_detail(asset_id):
        return render_template("6.html", asset=Asset.query.get_or_404(asset_id))

    @app.route("/assets/<int:asset_id>/technical")
    @login_required
    def asset_technical(asset_id):
        asset = Asset.query.get_or_404(asset_id)
        tech = TechnicalAssetDetail.query.filter_by(asset_id=asset_id).first()
        return render_template("7.html", asset=asset, tech=tech)

    @app.route("/assets/<int:asset_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_asset(asset_id):
        a = Asset.query.get_or_404(asset_id)
        if request.method == "POST":
            for f in ["name", "category", "status", "region", "site", "supplier", "manufacturer", "model", "criticality"]:
                setattr(a, f, request.form.get(f))
            a.purchase_cost = request.form.get("purchase_cost") or 0
            a.current_value = request.form.get("current_value") or 0
            a.expected_life_years = request.form.get("expected_life_years") or 10
            a.mileage = request.form.get("mileage") or 0
            db.session.commit()
            flash("Asset updated.", "success")
            return redirect(url_for("asset_detail", asset_id=a.id))
        return render_template("10.html", asset=a)

    @app.route("/assets/<int:asset_id>/history")
    @login_required
    def asset_history(asset_id):
        a = Asset.query.get_or_404(asset_id)
        return render_template(
            "9.html",
            asset=a,
            service_history=ServiceHistory.query.filter_by(asset_id=asset_id).order_by(ServiceHistory.service_date.desc()).all(),
            requests=ServiceRequest.query.filter_by(asset_id=asset_id).all(),
            costs=CostHistory.query.filter_by(asset_id=asset_id).all(),
        )

    @app.route("/assets/locations")
    @login_required
    def asset_locations():
        return render_template("3.html", locations=Location.query.order_by(Location.name).all(), assets=Asset.query.all())

    @app.route("/maintenance/request", methods=["GET", "POST"])
    @app.route("/maintenance/new-request", methods=["GET", "POST"])
    @login_required
    def create_service_request():
        if request.method == "POST":
            r = ServiceRequest(
                request_id=f"SR-{datetime.utcnow():%Y%m%d%H%M%S%f}",
                asset_id=request.form.get("asset_id") or None,
                title=request.form.get("title", "Service request"),
                description=request.form.get("description"),
                priority=request.form.get("priority", "Medium"),
                team=request.form.get("team"),
                source=request.form.get("source", "Portal"),
            )
            db.session.add(r)
            db.session.flush()
            db.session.add(ServiceAudit(service_request_id=r.id, action="Request created", actor=current_user.full_name, notes="Entered centralized maintenance pipeline."))
            db.session.commit()
            flash(f"{r.request_id} submitted.", "success")
            return redirect(url_for("service_requests"))
        return render_template("4.html", assets=Asset.query.all())

    @app.route("/maintenance/requests")
    @app.route("/service-requests")
    @login_required
    def service_requests():
        q = request.args.get("q", "").strip()
        query = ServiceRequest.query
        if q:
            query = query.filter(or_(ServiceRequest.request_id.like(f"%{q}%"), ServiceRequest.title.like(f"%{q}%"), ServiceRequest.team.like(f"%{q}%")))
        if request.args.get("status"):
            query = query.filter_by(status=request.args.get("status"))
        return render_template("5.html", service_requests=query.order_by(ServiceRequest.created_at.desc()).all())

    @app.post("/service-requests/<int:req_id>/status")
    @login_required
    def set_request_status(req_id):
        r = ServiceRequest.query.get_or_404(req_id)
        new = request.form.get("status", r.status)
        r.status = new
        now = datetime.utcnow()
        mapping = {"Accepted": "accepted_at", "In Progress": "started_at", "Completed": "completed_at", "Closed": "closed_at"}
        if new in mapping:
            setattr(r, mapping[new], now)
        db.session.add(ServiceAudit(service_request_id=r.id, action=f"Status changed to {new}", actor=current_user.full_name))
        db.session.commit()
        flash("Service request updated.", "success")
        return redirect(request.referrer or url_for("service_requests"))

    @app.route("/maintenance/audit")
    @login_required
    def service_audit():
        return render_template("11.html", audits=ServiceAudit.query.order_by(ServiceAudit.created_at.desc()).all())

    @app.route("/vendors", methods=["GET", "POST"])
    @login_required
    def vendors():
        if request.method == "POST":
            vendor_name = request.form.get("name", "").strip()
            if not vendor_name:
                flash("Vendor name is required.", "danger")
                return redirect(url_for("vendors"))
            vendor_code = request.form.get("vendor_code", "").strip() or f"VND-{datetime.utcnow():%Y%m%d%H%M%S%f}"
            vendor = Vendor(
                vendor_code=vendor_code,
                name=vendor_name,
                vendor_type=request.form.get("vendor_type"),
                contact_name=request.form.get("contact_name"),
                email=request.form.get("email"),
                phone=request.form.get("phone"),
                active=True,
            )
            db.session.add(vendor)
            db.session.commit()
            flash("Vendor saved.", "success")
            return redirect(url_for("vendors"))
        return render_template("12.html", vendors=Vendor.query.order_by(Vendor.name).all())

    @app.route("/parts", methods=["GET", "POST"])
    @login_required
    def parts():
        if request.method == "POST":
            db.session.add(
                Part(
                    part_number=request.form.get("part_number", ""),
                    name=request.form.get("name", ""),
                    manufacturer=request.form.get("manufacturer"),
                    model=request.form.get("model"),
                    quantity_on_hand=request.form.get("quantity_on_hand") or 0,
                    reorder_level=request.form.get("reorder_level") or 0,
                    unit_cost=request.form.get("unit_cost") or 0,
                    supplier_id=request.form.get("supplier_id") or None,
                )
            )
            db.session.commit()
            flash("Part saved.", "success")
            return redirect(url_for("parts"))
        return render_template(
            "14.html",
            parts=Part.query.order_by(Part.name).all(),
            vendors=Vendor.query.order_by(Vendor.name).all(),
            reports=ServiceReport.query.order_by(ServiceReport.report_date.desc()).limit(20).all(),
            third_party=ThirdPartyWorkOrder.query.order_by(ThirdPartyWorkOrder.created_at.desc()).limit(20).all(),
            assets=Asset.query.all(),
        )

    @app.route("/maintenance/consumables", methods=["GET", "POST"])
    @login_required
    def consumables():
        if request.method == "POST":
            db.session.add(
                Consumable(
                    asset_id=int(request.form.get("asset_id")),
                    item_name=request.form.get("item_name", ""),
                    manufacturer=request.form.get("manufacturer"),
                    model=request.form.get("model"),
                    quantity=request.form.get("quantity") or 0,
                    unit=request.form.get("unit", "unit"),
                    unit_cost=request.form.get("unit_cost") or 0,
                    used_at=date.fromisoformat(request.form.get("used_at")) if request.form.get("used_at") else date.today(),
                )
            )
            db.session.commit()
            flash("Consumable usage recorded.", "success")
            return redirect(url_for("consumables"))
        return render_template("15.html", assets=Asset.query.all(), consumables=Consumable.query.order_by(Consumable.used_at.desc()).all())

    @app.route("/maintenance/preventive", methods=["GET", "POST"])
    @login_required
    def preventive():
        if request.method == "POST":
            db.session.add(
                MaintenanceSchedule(
                    asset_id=int(request.form.get("asset_id")),
                    task=request.form.get("task", ""),
                    frequency=request.form.get("frequency"),
                    priority=request.form.get("priority", "Medium"),
                    due_date=date.fromisoformat(request.form.get("due_date")) if request.form.get("due_date") else None,
                )
            )
            db.session.commit()
            flash("PM schedule created.", "success")
            return redirect(url_for("preventive"))
        return render_template(
            "16.html",
            schedules=MaintenanceSchedule.query.order_by(MaintenanceSchedule.due_date).all(),
            assets=Asset.query.all(),
            executions=PMExecution.query.order_by(PMExecution.execution_date.desc()).limit(20).all(),
        )

    @app.post("/maintenance/preventive/<int:schedule_id>/complete")
    @login_required
    def complete_pm(schedule_id):
        s = MaintenanceSchedule.query.get_or_404(schedule_id)
        s.status = "Completed"
        s.last_completed = date.today()
        db.session.add(
            PMExecution(
                schedule_id=s.id,
                asset_id=s.asset_id,
                executed_by=current_user.full_name,
                execution_date=date.today(),
                status="Completed",
                findings=request.form.get("findings"),
                labor_hours=request.form.get("labor_hours") or 0,
                cost=request.form.get("cost") or 0,
            )
        )
        db.session.commit()
        flash("PM execution recorded.", "success")
        return redirect(url_for("preventive"))

    @app.route("/maintenance/intelligence")
    @app.route("/intelligence")
    def _mi():
        return redirect(url_for("maintenance_intelligence"))

    @app.route("/maintenance-intelligence")
    @login_required
    def maintenance_intelligence():
        records = MaintenanceIntelligence.query.order_by(MaintenanceIntelligence.risk_score.desc()).all()
        preds = FailurePrediction.query.order_by(FailurePrediction.probability.desc()).all()
        return render_template("8.html", records=records, predictions=preds)

    @app.route("/strategic-intelligence")
    @app.route("/failure-forecast")
    @login_required
    def failure_forecast():
        assets = Asset.query.all()
        decisions = CapitalDecision.query.order_by(CapitalDecision.decision_score.desc()).all()
        recs = IntelligenceRecommendation.query.order_by(IntelligenceRecommendation.priority.desc()).all()
        return render_template("17.html", assets=assets, decisions=decisions, recommendations=recs, predictions=FailurePrediction.query.order_by(FailurePrediction.probability.desc()).all())

    @app.route("/capital-allocation", methods=["GET", "POST"])
    @login_required
    def capital_allocation():
        if request.method == "POST":
            db.session.add(
                CapitalDecision(
                    asset_id=int(request.form.get("asset_id")),
                    decision=request.form.get("decision"),
                    recommended_capex=request.form.get("recommended_capex") or 0,
                    expected_life_extension_years=request.form.get("life_extension") or 0,
                    expected_annual_saving=request.form.get("saving") or 0,
                    decision_score=request.form.get("score") or 0,
                    rationale=request.form.get("rationale"),
                    decision_date=date.today(),
                )
            )
            db.session.commit()
            flash("Capital decision saved.", "success")
            return redirect(url_for("capital_allocation"))
        return render_template(
            "17.html",
            assets=Asset.query.all(),
            decisions=CapitalDecision.query.order_by(CapitalDecision.decision_score.desc()).all(),
            recommendations=IntelligenceRecommendation.query.all(),
            predictions=FailurePrediction.query.all(),
        )

    @app.route("/notifications")
    @login_required
    def alerts():
        return render_template("13.html", notifications=Notification.query.order_by(Notification.created_at.desc()).all())

    @app.route("/reports")
    @app.route("/maintenance/reports")
    @login_required
    def reports_analytics():
        return render_template("16.html", schedules=MaintenanceSchedule.query.all(), assets=Asset.query.all(), executions=PMExecution.query.all())

    @app.route("/maintenance/workflow")
    @login_required
    def workflow():
        return redirect(url_for("parts"))

    @app.route("/item-catalog")
    @login_required
    def item_catalog():
        return redirect(url_for("asset_register"))

    @app.route("/my-items")
    @login_required
    def my_items():
        return redirect(url_for("asset_register"))

    @app.route("/work-orders")
    @login_required
    def work_orders():
        return redirect(url_for("service_requests"))

    @app.route("/setup")
    @login_required
    def setup():
        return redirect(url_for("dashboard"))

    @app.route("/settings")
    @login_required
    def settings():
        return redirect(url_for("dashboard"))

    @app.route("/help")
    def help_page():
        return redirect(url_for("home"))

    @app.route("/api/qr/<int:asset_id>")
    @login_required
    def asset_qr(asset_id):
        import qrcode
        a = Asset.query.get_or_404(asset_id)
        img = qrcode.make(url_for("asset_detail", asset_id=a.id, _external=True))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return send_file(buf, mimetype="image/png")

    @app.route("/export/assets.csv")
    @login_required
    def export_assets():
        out = io.StringIO()
        w = csv.writer(out)
        w.writerow(["Asset Tag", "Name", "Category", "Status", "Region", "Site", "Supplier", "Criticality", "Current Value"])
        for a in Asset.query.all():
            w.writerow([a.asset_tag, a.name, a.category, a.status, a.region, a.site, a.supplier, a.criticality, a.current_value])
        return Response(out.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=assets.csv"})
