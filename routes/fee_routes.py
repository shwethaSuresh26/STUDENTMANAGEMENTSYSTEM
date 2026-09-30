from datetime import datetime, date, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import db, FeeRecord, FeePayment, Student, Department
from utils import login_required, log_activity

fee_bp = Blueprint('fees', __name__, url_prefix='/fees')

@fee_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    dept_id = request.args.get('department_id', type=int)

    query = FeeRecord.query.join(Student)

    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            (Student.student_id.ilike(search_fmt)) |
            (Student.first_name.ilike(search_fmt)) |
            (Student.last_name.ilike(search_fmt)) |
            (FeeRecord.title.ilike(search_fmt))
        )
    if category:
        query = query.filter(FeeRecord.fee_category == category)
    if status:
        query = query.filter(FeeRecord.status == status)
    if dept_id:
        query = query.filter(Student.department_id == dept_id)

    records = query.order_by(FeeRecord.created_at.desc()).all()
    departments = Department.query.order_by(Department.name).all()

    # Aggregate financial numbers
    total_invoiced = sum(r.total_amount for r in records)
    total_collected = sum(r.paid_amount for r in records)
    total_pending = sum(r.balance_amount for r in records)

    categories = [
        'Tuition Fee', 'Exam Fee', 'Library Fee', 
        'Hostel Fee', 'Transport Fee', 'Other Fees'
    ]

    return render_template(
        'fees/index.html',
        records=records,
        departments=departments,
        categories=categories,
        search=search,
        selected_category=category,
        selected_status=status,
        selected_dept=dept_id,
        total_invoiced=total_invoiced,
        total_collected=total_collected,
        total_pending=total_pending
    )


@fee_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    students = Student.query.filter_by(status='Active').order_by(Student.student_id).all()
    categories = ['Tuition Fee', 'Exam Fee', 'Library Fee', 'Hostel Fee', 'Transport Fee', 'Other Fees']

    if request.method == 'POST':
        student_id = request.form.get('student_id', type=int)
        fee_category = request.form.get('fee_category', 'Tuition Fee')
        title = request.form.get('title', '').strip()
        total_amount = request.form.get('total_amount', type=float)
        initial_paid = request.form.get('initial_paid', 0.0, type=float)
        due_date_str = request.form.get('due_date')
        payment_method = request.form.get('payment_method', 'Cash')
        transaction_id = request.form.get('transaction_id', '').strip()
        notes = request.form.get('notes', '').strip()

        if not student_id or not title or not total_amount:
            flash('Please specify student, fee title, and total amount.', 'danger')
            return render_template('fees/add.html', students=students, categories=categories)

        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else date.today()
        except ValueError:
            due_date = date.today()

        initial_paid = min(initial_paid, total_amount)
        balance = total_amount - initial_paid

        fee_record = FeeRecord(
            student_id=student_id,
            fee_category=fee_category,
            title=title,
            total_amount=total_amount,
            paid_amount=initial_paid,
            balance_amount=balance,
            status='Paid' if balance == 0 else ('Partially Paid' if initial_paid > 0 else 'Pending'),
            due_date=due_date
        )
        db.session.add(fee_record)
        db.session.flush()

        payment_entry = None
        if initial_paid > 0:
            payment_entry = FeePayment(
                fee_record_id=fee_record.id,
                amount=initial_paid,
                payment_method=payment_method,
                transaction_id=transaction_id or f"TXN{int(datetime.now(timezone.utc).timestamp())}",
                payment_date=datetime.now(timezone.utc),
                notes=notes,
                recorded_by=session.get('full_name', 'Admin')
            )
            db.session.add(payment_entry)

        db.session.commit()

        stu = db.session.get(Student, student_id)
        stu_name = stu.full_name if stu else 'Student'
        log_activity('Fees', f"Created fee invoice '{title}' (${total_amount}) for {stu_name}.", 'bi-receipt')
        
        flash('Fee invoice created successfully!', 'success')
        if payment_entry:
            return redirect(url_for('fees.receipt', payment_id=payment_entry.id))
        return redirect(url_for('fees.index'))

    return render_template('fees/add.html', students=students, categories=categories)


@fee_bp.route('/pay/<int:fee_id>', methods=['POST'])
@login_required
def pay(fee_id):
    fee = db.get_or_404(FeeRecord, fee_id)
    
    amount = request.form.get('amount', type=float)
    payment_method = request.form.get('payment_method', 'Cash')
    transaction_id = request.form.get('transaction_id', '').strip()
    notes = request.form.get('notes', '').strip()

    if not amount or amount <= 0:
        flash('Payment amount must be greater than zero.', 'danger')
        return redirect(url_for('fees.index'))

    if amount > fee.balance_amount:
        flash(f"Payment amount (${amount:.2f}) cannot exceed pending balance (${fee.balance_amount:.2f}).", 'warning')
        return redirect(url_for('fees.index'))

    payment = FeePayment(
        fee_record_id=fee.id,
        amount=amount,
        payment_method=payment_method,
        transaction_id=transaction_id or f"TXN{int(datetime.now(timezone.utc).timestamp())}",
        payment_date=datetime.now(timezone.utc),
        notes=notes,
        recorded_by=session.get('full_name', 'Admin')
    )
    db.session.add(payment)
    db.session.flush()

    fee.update_balance_and_status()
    db.session.commit()

    log_activity('Fees', f"Received payment of ${amount:.2f} for {fee.title} from {fee.student.full_name}.", 'bi-cash-coin')
    flash(f"Payment of ${amount:.2f} successfully recorded!", 'success')
    return redirect(url_for('fees.receipt', payment_id=payment.id))


@fee_bp.route('/receipt/<int:payment_id>')
@login_required
def receipt(payment_id):
    payment = db.get_or_404(FeePayment, payment_id)
    fee_record = payment.fee_record
    student = fee_record.student

    return render_template(
        'fees/receipt.html',
        payment=payment,
        fee=fee_record,
        student=student,
        generated_date=payment.payment_date.strftime('%d-%b-%Y %I:%M %p')
    )


@fee_bp.route('/student/<int:student_id>')
@login_required
def student_ledger(student_id):
    student = db.get_or_404(Student, student_id)
    fee_records = FeeRecord.query.filter_by(student_id=student_id).order_by(FeeRecord.due_date.desc()).all()

    total_fees = sum(f.total_amount for f in fee_records)
    total_paid = sum(f.paid_amount for f in fee_records)
    total_due = sum(f.balance_amount for f in fee_records)

    return render_template(
        'fees/student_ledger.html',
        student=student,
        fee_records=fee_records,
        total_fees=total_fees,
        total_paid=total_paid,
        total_due=total_due
    )


@fee_bp.route('/delete/<int:fee_id>', methods=['POST'])
@login_required
def delete(fee_id):
    fee = db.get_or_404(FeeRecord, fee_id)
    title = fee.title
    db.session.delete(fee)
    db.session.commit()
    log_activity('Fees', f"Deleted fee invoice '{title}'.", 'bi-trash')
    flash(f"Fee record '{title}' deleted.", 'info')
    return redirect(url_for('fees.index'))
