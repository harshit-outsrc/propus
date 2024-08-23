from propus.aws.ssm import AWS_SSM
from propus.aws.s3 import AWS_S3
from propus.gsuite.user_directory import UserDirectory
from propus.gsuite.constants import CALBRIGHT_COLLEGE_PUBLIC_STATIC_S3_BUCKET, STUDENT_THUMBNAIL_FOLDER_PATH
from propus import Logging

logger = Logging.get_logger("propus/gsuite/user_directory.py")


def fetch_student_photo(user_id):
    """
    Fetches the user's Google profile picture information using the UserDirectory Wrapper Class

    Args:
        user_id: User ID or email for identifying the user.

    Returns:
        UserPhoto object(https://developers.google.com/admin-sdk/directory/reference/rest/v1/UserPhoto) that is a
        dictionary containing user photo information.
        example: {
            'kind': 'admin#directory#user#photo',
            'id': '106513579493353403060',
            'etag': '"rNVw6s4PoMfwBW7LDetdt3OSpR6BZyHF4-IZC6b9NGw/OW05Kxp-sIwFzJUvFU5B6k8DKww"',
            'primaryEmail': 'raghav.naswa@calbrightcollege.org',
            'mimeType': 'image/jpeg',
            'height': 96,
            'width': 96,
            'photoData':'IMAGE IN BASE 64 ENCODED FORMAT'
        }

    Raises:
        Exception: If there is an error fetching the user photo.

    """
    student_accounts = UserDirectory.build(
        AWS_SSM.build().get_param("gsuite.calbright-student.users", param_type="json")
    )
    try:
        result = student_accounts.fetch_profile_picture(user_id)
    except Exception as err:
        raise err
    return result


def fetch_student_photo_url(user_email, ccc_id):
    """
    Checks if the user's profile picture exists in an S3 bucket, fetches it if not, and uploads it to the bucket.

    Args:
        user_email: User's email for identifying the user.
        ccc_id: Unique identifier for the user.

    Returns:
        String: photo URL

    Raises:
        Exception: If there is an error fetching the default user photo.
    """
    # Initialize S3 client and resource using the S3 class from the provided file
    s3 = AWS_S3.build()

    # Define S3 bucket information
    aws_region = s3.s3_client.meta.region_name
    s3_endpoint_url = (
        f"https://s3.{aws_region}.amazonaws.com/{CALBRIGHT_COLLEGE_PUBLIC_STATIC_S3_BUCKET}/"
        f"{STUDENT_THUMBNAIL_FOLDER_PATH}"
    )

    try:
        # Check if the file with the given CCC_ID exists in the S3 bucket
        if s3.s3_file_exists(
            CALBRIGHT_COLLEGE_PUBLIC_STATIC_S3_BUCKET, f"{STUDENT_THUMBNAIL_FOLDER_PATH}/{ccc_id}.png"
        ):
            return f"{s3_endpoint_url}{ccc_id}.png"
        elif s3.s3_file_exists(
            CALBRIGHT_COLLEGE_PUBLIC_STATIC_S3_BUCKET, f"{STUDENT_THUMBNAIL_FOLDER_PATH}/{ccc_id}.jpeg"
        ):
            return f"{s3_endpoint_url}{ccc_id}.jpeg"
    except Exception as ex:
        logger.info(f"Couln't get user image for {user_email}, switching to default avatar: {ex}")
    return AWS_SSM.build().get_param("student.default_user_avatar")
