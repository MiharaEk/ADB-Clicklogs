#created to run the queries using firestore database data directly (as per the assignment updates done on 11-04-2026)

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#a.Mean duration by platform (Android Vs PC)
def mean_duration_by_platform():
    results = {}
    for platform in ["android", "pc"]:
        docs = db.collection("tap_logs").where("devicePlatform", "==", platform).stream()
        durations = [doc.to_dict()["duration"] for doc in docs]
        if durations:
            results[platform] = sum(durations) / len(durations)
    return results

print("a.Mean duration by platform:", mean_duration_by_platform())


#b.Mean duration by interface (eedbackshown vs nofeedback)
def mean_duration_by_interface():
    results = {}
    for interface in ["feedbackshown", "nofeedback"]:
        docs = db.collection("tap_logs").where("interfaceType", "==", interface).stream()
        durations = [doc.to_dict()["duration"] for doc in docs]
        if durations:
            results[interface] = sum(durations) / len(durations)
    return results

print("b.Mean duration by interface:", mean_duration_by_interface())


#c. Completion vs drop‑off
def completion_vs_dropout():
    sessions = {}
    docs = db.collection("tap_logs").stream()
    for doc in docs:
        data = doc.to_dict()
        sid = data["sessionId"]
        if sid not in sessions:
            sessions[sid] = set()
        sessions[sid].add(data["interfaceType"])

    completed_both = sum(1 for interfaces in sessions.values() if len(interfaces) == 2)
    dropped_off = sum(1 for interfaces in sessions.values() if len(interfaces) == 1)

    return {"completedBoth": completed_both, "droppedOff": dropped_off}

print("c.Completion vs drop-off:", completion_vs_dropout())

