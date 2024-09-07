import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# Use the application default credentials.
cred = credentials.ApplicationDefault()

firebase_admin.initialize_app(cred)
db = firestore.client()

docs = (
    db.collection("/Content/")
    # .where(filter=FieldFilter("sortOrder", "<=", "50"))
    .stream()
)

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
