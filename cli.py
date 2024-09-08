import click
import ujson
import firebase_admin
from firebase_admin import firestore


@click.group()
@click.option("--collection", default="/")
@click.pass_context
def cli(ctx, collection):
    ctx.obj = {
        "py": firebase_admin.initialize_app(),
        "db": firestore.client(),
        "collection": collection,
    }

@cli.command()
@click.pass_obj 
def root(obj):
    print(f"root: {obj['collection']}")
    docs = obj["db"].collections()
    for doc in docs:
        print(doc.id)   


@cli.command()
@click.argument("collection")
@click.pass_obj
def list(obj, collection):
    print(f"list: {collection}")
    docs = obj["db"].collection(collection).stream()
    for doc in docs:
        print(f'{doc.id} "{doc._data['name']}"')


@cli.command()
@click.argument("doc_id")
@click.pass_obj
def get(obj, doc_id):
    doc = obj["db"].collection(obj["collection"]).document(doc_id).get()
    text = ujson.dumps(doc.to_dict(), indent=2)
    print(text)

@cli.command()
@click.argument("in_collection")
@click.argument("out_collection")
@click.pass_obj
def copy(obj, in_collection, out_collection):
    print(f"copy {in_collection} => {out_collection}")
    try:
        docs = obj["db"].collection(in_collection).get()
        print(f"Found {len(docs)} documents")
    except Exception as e:
        print(f"Error on input {in_collection}: {e}")
        return
    
    try:
        for doc in docs:
            doc_dict = doc.to_dict()
            # del doc_dict["id"]
            print(f"Adding {doc_dict["name"]} to {out_collection}")
            # print(doc_dict)
            obj["db"].collection(out_collection).add(doc_dict)
    except Exception as e:
        print(f"Error on output {out_collection}: {e}")
        return
  

if __name__ == "__main__":
    cli()
