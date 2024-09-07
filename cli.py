import click
import ujson
import firebase_admin
from firebase_admin import firestore

@click.group()
@click.option("--collection", default="Content")
@click.pass_context
def cli(ctx, collection):
    ctx.obj = {
        "app" : firebase_admin.initialize_app(),
        "db" : firestore.client(),
        "collection" : collection,
    }

@cli.command()
@click.pass_obj
def list(obj):
  docs = obj["db"].collection(obj["collection"]).stream()
  for doc in docs:
     print(f"{doc.id}")


@cli.command()
@click.argument("doc_id")
@click.pass_obj
def get(obj, doc_id):
  doc = obj["db"].collection(obj["collection"]).document(doc_id).get()
  text = ujson.dumps(doc.to_dict(), indent=2)
  print(text)

if __name__ == "__main__":
   cli()