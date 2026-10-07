from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class User(TimestampMixin, UserMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); full_name=db.Column(db.String(150),nullable=False); email=db.Column(db.String(190),unique=True,nullable=False,index=True); password_hash=db.Column(db.String(255),nullable=False); role=db.Column(db.String(50),default="Manager"); organization=db.Column(db.String(190),default="AB Afric Integrated Services"); active=db.Column(db.Boolean,default=True)
    def set_password(self,p): self.password_hash=generate_password_hash(p)
    def check_password(self,p): return check_password_hash(self.password_hash,p)

class Location(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(150),nullable=False); region=db.Column(db.String(100)); site=db.Column(db.String(150)); address=db.Column(db.String(255)); latitude=db.Column(db.Float); longitude=db.Column(db.Float); manager=db.Column(db.String(150)); active=db.Column(db.Boolean,default=True)

class Vendor(TimestampMixin, db.Model):
    __tablename__ = "vendor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_code = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(190), nullable=False)
    vendor_type = db.Column(db.String(80))
    contact_name = db.Column(db.String(150))
    contact_person = db.Column(db.String(150))
    email = db.Column(db.String(190))
    phone = db.Column(db.String(80))
    address = db.Column(db.String(255))
    region = db.Column(db.String(100))
    rating = db.Column(db.Float)
    active = db.Column(db.Boolean)

class Asset(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_tag=db.Column(db.String(80),unique=True,nullable=False,index=True); name=db.Column(db.String(190),nullable=False); category=db.Column(db.String(100)); status=db.Column(db.String(50),default="Operational"); region=db.Column(db.String(100)); site=db.Column(db.String(150)); supplier=db.Column(db.String(150)); manufacturer=db.Column(db.String(150)); model=db.Column(db.String(150)); criticality=db.Column(db.String(30),default="Medium"); purchase_cost=db.Column(db.Numeric(14,2),default=0); current_value=db.Column(db.Numeric(14,2),default=0); annual_maintenance_budget=db.Column(db.Numeric(14,2),default=0); install_date=db.Column(db.Date); commissioning_date=db.Column(db.Date); expected_life_years=db.Column(db.Integer,default=10); mileage=db.Column(db.Integer,default=0); latitude=db.Column(db.Float); longitude=db.Column(db.Float); thumbnail_url=db.Column(db.String(500)); location_id=db.Column(db.Integer,db.ForeignKey("location.id")); vendor_id=db.Column(db.Integer,db.ForeignKey("vendor.id")); location=db.relationship("Location",backref="assets"); vendor=db.relationship("Vendor",backref="assets")

class TechnicalAssetDetail(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),unique=True,nullable=False); asset_type=db.Column(db.String(100)); serial_number=db.Column(db.String(120)); safety_status=db.Column(db.String(60)); structure_condition=db.Column(db.String(60)); refrigeration_condition=db.Column(db.String(60)); compressor_condition=db.Column(db.String(60)); refrigerant_type=db.Column(db.String(80)); refrigerant_charge=db.Column(db.Float); operating_hours=db.Column(db.Float,default=0); temperature_range=db.Column(db.String(80)); inspection_notes=db.Column(db.Text); asset=db.relationship("Asset",backref=db.backref("technical_detail",uselist=False))

class ServiceRequest(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); request_id=db.Column(db.String(40),unique=True,nullable=False,index=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id")); title=db.Column(db.String(255),nullable=False); description=db.Column(db.Text); priority=db.Column(db.String(30),default="Medium"); status=db.Column(db.String(40),default="Submitted"); team=db.Column(db.String(100)); assigned_to=db.Column(db.String(150)); source=db.Column(db.String(50),default="Portal"); created_at=db.Column(db.DateTime,default=datetime.utcnow,nullable=False); accepted_at=db.Column(db.DateTime); started_at=db.Column(db.DateTime); completed_at=db.Column(db.DateTime); closed_at=db.Column(db.DateTime); asset=db.relationship("Asset",backref="service_requests")

class ServiceAudit(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); service_request_id=db.Column(db.Integer,db.ForeignKey("service_request.id"),nullable=False); action=db.Column(db.String(120),nullable=False); actor=db.Column(db.String(150)); notes=db.Column(db.Text); service_request=db.relationship("ServiceRequest",backref="audit_entries")

class ServiceHistory(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); service_request_id=db.Column(db.Integer,db.ForeignKey("service_request.id")); service_type=db.Column(db.String(100)); summary=db.Column(db.Text); response_minutes=db.Column(db.Integer); repair_minutes=db.Column(db.Integer); outcome=db.Column(db.String(100)); cost=db.Column(db.Numeric(14,2),default=0); performed_by=db.Column(db.String(150)); service_date=db.Column(db.Date); asset=db.relationship("Asset",backref="service_history")

class Part(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); part_number=db.Column(db.String(100),unique=True,nullable=False); name=db.Column(db.String(190),nullable=False); manufacturer=db.Column(db.String(150)); model=db.Column(db.String(150)); unit=db.Column(db.String(40),default="unit"); quantity_on_hand=db.Column(db.Float,default=0); reorder_level=db.Column(db.Float,default=0); unit_cost=db.Column(db.Numeric(14,2),default=0); supplier_id=db.Column(db.Integer,db.ForeignKey("vendor.id")); supplier=db.relationship("Vendor",backref="parts")

class PartUsage(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); part_id=db.Column(db.Integer,db.ForeignKey("part.id"),nullable=False); service_request_id=db.Column(db.Integer,db.ForeignKey("service_request.id")); quantity=db.Column(db.Float,default=1); unit_cost=db.Column(db.Numeric(14,2),default=0); used_at=db.Column(db.Date,nullable=False); notes=db.Column(db.Text); asset=db.relationship("Asset",backref="part_usages"); part=db.relationship("Part",backref="usages")

class MaintenanceSchedule(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); task=db.Column(db.String(255),nullable=False); frequency=db.Column(db.String(80)); priority=db.Column(db.String(30),default="Medium"); due_date=db.Column(db.Date); status=db.Column(db.String(40),default="Scheduled"); last_completed=db.Column(db.Date); asset=db.relationship("Asset",backref="maintenance_schedules")

class PMExecution(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); schedule_id=db.Column(db.Integer,db.ForeignKey("maintenance_schedule.id"),nullable=False); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); executed_by=db.Column(db.String(150)); execution_date=db.Column(db.Date,nullable=False); status=db.Column(db.String(40),default="Completed"); findings=db.Column(db.Text); labor_hours=db.Column(db.Float,default=0); cost=db.Column(db.Numeric(14,2),default=0)

class Consumable(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); item_name=db.Column(db.String(190),nullable=False); manufacturer=db.Column(db.String(150)); model=db.Column(db.String(150)); quantity=db.Column(db.Float,default=0); unit=db.Column(db.String(40),default="unit"); unit_cost=db.Column(db.Numeric(14,2),default=0); used_at=db.Column(db.Date,nullable=False); asset=db.relationship("Asset",backref="consumables")

class LaborEntry(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id")); service_request_id=db.Column(db.Integer,db.ForeignKey("service_request.id")); technician=db.Column(db.String(150),nullable=False); role=db.Column(db.String(100)); hours=db.Column(db.Float,default=0); hourly_rate=db.Column(db.Numeric(14,2),default=0); work_date=db.Column(db.Date,nullable=False); notes=db.Column(db.Text)

class CostHistory(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); service_request_id=db.Column(db.Integer,db.ForeignKey("service_request.id")); cost_type=db.Column(db.String(80)); amount=db.Column(db.Numeric(14,2),nullable=False); currency=db.Column(db.String(10),default="USD"); cost_date=db.Column(db.Date,nullable=False); description=db.Column(db.Text)

class ServiceReport(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); service_request_id=db.Column(db.Integer,db.ForeignKey("service_request.id")); report_no=db.Column(db.String(80),unique=True,nullable=False); service_type=db.Column(db.String(100)); mileage=db.Column(db.Integer); man_hours=db.Column(db.Float,default=0); total_cost=db.Column(db.Numeric(14,2),default=0); outcome=db.Column(db.String(120)); findings=db.Column(db.Text); report_date=db.Column(db.Date,nullable=False)

class ThirdPartyWorkOrder(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); service_request_id=db.Column(db.Integer,db.ForeignKey("service_request.id")); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); vendor_id=db.Column(db.Integer,db.ForeignKey("vendor.id"),nullable=False); stage=db.Column(db.String(60),default="Inspection"); quote_amount=db.Column(db.Numeric(14,2),default=0); approved_amount=db.Column(db.Numeric(14,2),default=0); mobilization_date=db.Column(db.Date); completion_date=db.Column(db.Date); approval_status=db.Column(db.String(50),default="Pending"); notes=db.Column(db.Text)

class AssetMovement(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); from_location_id=db.Column(db.Integer,db.ForeignKey("location.id")); to_location_id=db.Column(db.Integer,db.ForeignKey("location.id")); movement_date=db.Column(db.Date,nullable=False); reason=db.Column(db.String(190)); reference=db.Column(db.String(100)); moved_by=db.Column(db.String(150))

class Notification(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); channel=db.Column(db.String(30),nullable=False); recipient=db.Column(db.String(190),nullable=False); subject=db.Column(db.String(255)); message=db.Column(db.Text); status=db.Column(db.String(30),default="Queued"); sent_at=db.Column(db.DateTime)

class FailurePrediction(TimestampMixin, db.Model):
    __tablename__ = "failure_prediction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asset_id = db.Column(
        db.Integer,
        db.ForeignKey("asset.id"),
        nullable=False
    )

    predicted_failure_date = db.Column(db.Date)
    probability = db.Column(db.Float, default=0)
    severity = db.Column(db.String(40))
    failure_mode = db.Column(db.String(150))
    contributing_factors = db.Column(db.Text)
    recommended_action = db.Column(db.String(255))
    status = db.Column(db.String(50))
    model_version = db.Column(db.String(100))

    asset = db.relationship(
        "Asset",
        backref="failure_predictions"
    )

class MaintenanceIntelligence(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); health_score=db.Column(db.Float,default=0); reliability_score=db.Column(db.Float,default=0); annual_maintenance_forecast=db.Column(db.Numeric(14,2),default=0); economic_impact=db.Column(db.Numeric(14,2),default=0); risk_score=db.Column(db.Float,default=0); recommendation=db.Column(db.String(190)); rationale=db.Column(db.Text); as_of_date=db.Column(db.Date,nullable=False); asset=db.relationship("Asset",backref="intelligence_records")

class CapitalDecision(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id"),nullable=False); decision=db.Column(db.String(30),nullable=False); recommended_capex=db.Column(db.Numeric(14,2),default=0); expected_life_extension_years=db.Column(db.Float,default=0); expected_annual_saving=db.Column(db.Numeric(14,2),default=0); decision_score=db.Column(db.Float,default=0); rationale=db.Column(db.Text); decision_date=db.Column(db.Date,nullable=False); status=db.Column(db.String(40),default="Proposed"); asset=db.relationship("Asset",backref="capital_decisions")

class IntelligenceRecommendation(TimestampMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True); asset_id=db.Column(db.Integer,db.ForeignKey("asset.id")); recommendation_type=db.Column(db.String(100)); recommendation=db.Column(db.Text,nullable=False); priority=db.Column(db.String(30),default="Medium"); expected_value=db.Column(db.Numeric(14,2),default=0); status=db.Column(db.String(40),default="Open"); due_date=db.Column(db.Date); asset=db.relationship("Asset",backref="recommendations")
