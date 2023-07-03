from django.core.mail import send_mail
from django_project import settings


def send_leave_notification_mail(leave):
    """
    Sends a notification email to the HR-designated employees
    when an employee requests a leave.

    Args: leave (Leave)
    Takes the Leave object,representing the leave request as argument

    Returns: None
    """
    subject = "Leave Request Notification"
    message = (
        f"Employee {leave.employee.full_name()} has requested a leave.\n"
        f"Leave details : \n{leave.leave_details()}"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = ["nadeemmuhammad.work@gmail.com"]
    # mail ids of HR designated employees
    print(from_email)
    send_mail(subject, message, from_email, to_emails)


def send_leave_status_email(leave):
    """
    Sends a notification email to the requested employee
    regarding the status of their leave request.

    Args: leave (Leave)
    Takes the Leave object,representing the leave request as argument

    Returns: None
    """
    subject = "Leave Request Status"
    if leave.is_approved:
        status = "Approved"
    else:
        status = "Rejected"
    message = f"Your leave request has been {status}."
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = leave.employee.email

    send_mail(subject, message, from_email, [to_email])
