import threading
from typing import Any, List

from google.cloud import firestore
from google.cloud.firestore_v1.watch import DocumentChange, ChangeType
from tqdm import tqdm
from proto.datetime_helpers import DatetimeWithNanoseconds


def add_progress_listener(job_doc: firestore.DocumentReference, seq_count: int):
    bar = tqdm(total=100)

    def callback(docs: List[firestore.DocumentSnapshot],
                 changes: List[DocumentChange],
                 _: DatetimeWithNanoseconds):
        for document, change in zip(docs, changes):
            if change.type in {ChangeType.MODIFIED}:
                data = document.to_dict()
                import logging
                logging.debug(f'on_snapshot() called with {data}')
                if 'status' not in data:
                    continue
                status = data['status']
                if status == 'MSA_QUEUE':
                    bar.bar_suffix = 'MSA Queue'
                    bar.update(1)
                elif status == 'MSA_COMPLETE':
                    bar.bar_suffix = 'MSA Complete'
                    bar.progress = 50
                elif status == 'FOLDING':
                    bar.bar_suffix = 'Folding'
                    bar.progress = 51
                elif status == 'DONE':
                    bar.bar_suffix = 'Done'
                    bar.progress = 100
                    bar.close()

    sequences: firestore.CollectionReference = job_doc.collection('sequences')
    folding_progress = [0 for _ in range(seq_count)]

    def seq_callback(docs: List[firestore.DocumentSnapshot],
                     changes: List[DocumentChange],
                     _: DatetimeWithNanoseconds):
        for document, change in zip(docs, changes):
            if change.type in {ChangeType.MODIFIED}:
                data = document.to_dict()
                if 'progress' not in data:
                    return
                folding_progress[int(document.id)] = data['progress']['current']
                current_progress = sum(folding_progress) / (seq_count * data['progress']['total'])
                bar.progress = 50 + (50 * current_progress)

                bar.bar_suffix = f'Folding sequence {document.id}'

    job_doc.on_snapshot(callback)
    sequences.on_snapshot(seq_callback)


def field(doc: firestore.DocumentReference, *field_names: str) -> Any:
    """
    Watches the given fields in the document for changes and returns when one of the desired
    fields has changed.
    """
    event = threading.Event()
    retval = None

    def callback(docs: List[firestore.DocumentSnapshot],
                 changes: List[DocumentChange],
                 _: DatetimeWithNanoseconds):
        for document, change in zip(docs, changes):
            if change.type in {ChangeType.ADDED, ChangeType.MODIFIED}:
                data = document.to_dict()
                result = {field_name: data[field_name] for field_name in field_names if field_name in data}
                if result:
                    nonlocal retval
                    retval = result
                    event.set()

    doc.on_snapshot(callback)

    result = doc.get(field_names).to_dict()
    if result:  # the document already has the fields we are looking for
        return result

    event.wait()
    return retval
