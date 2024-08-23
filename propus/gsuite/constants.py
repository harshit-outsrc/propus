CALBRIGHT_COLLEGE_PUBLIC_STATIC_S3_BUCKET = "static.calbrightcollege.org"
STUDENT_THUMBNAIL_FOLDER_PATH = "assets/students/thumbnails/"
STUDENT_AVATARS_PATH = "assets/student-avatars/"

# G Suite Enterprise for Education
# According to https://developers.google.com/admin-sdk/licensing/v1/how-tos/products
# Product Name: G Suite Enterprise for Education
# Product ID: 101031
GSE_PRODUCT_ID = "101031"
# SKU Name: G Suite Enterprise for Education (Student)
# SKU ID: 1010310003
GSE_SKU_ID = "1010310003"
# If they're not in this OU and they have a GSEL, we revoke it.
GSE_LICENSED_OU = "Enrolled Students"

USER_KEY_MAPPING = {
    "agreed_to_terms": "agreedToTerms",
    "suspended": "suspended",
    "first_name": "givenName",
    "last_name": "familyName",
    "personal_email": "address",
    "phone_number": "value",
    "org_unit_path": "orgUnitPath",
}
