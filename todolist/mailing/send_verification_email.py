from textwrap import dedent

from core.models import User
from jinja_templates import templates
from mailing.send_email import send_email


async def send_verification_email(
    user: User,
    verification_token: str,
    verification_link: str,
):
    recipient = user.email
    subject = "Confirm your email for site.com"

    plain_content = dedent(
        f"""\
        Dear {recipient},
        
        Please follow the link to verify your email:
        {verification_link}
        
        Use this token to verify your email:
        {verification_token}
        
        Your site admin,
        copy 2026.
        """
    )

    template = templates.get_template("mailing/email-verify/verification_email.html")
    context = {
        "user": user,
        "verification_link": verification_link,
        "verification_token": verification_token,
    }
    html_content = template.render(
        context=context,
    )

    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
