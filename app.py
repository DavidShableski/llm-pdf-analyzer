#David Shableski
#dbshableski@gmail.com
#7/7/2025
#You upload a PDF, it automatically splits and indexes the text into a Chroma vector store, then lets you ask natural-language questions. 
# Answers appear in seconds with page-level source references and a loading spinner.

from flask import Flask, request, render_template, session, redirect, url_for
import os
import uuid

from populate_database import load_documents, split_documents, add_to_chroma
from analyzer          import query_rag

DATA_PATH   = "data"
BASE_CHROMA = "chroma"

app = Flask(__name__)
#ensure cookies are HTTP only and in production secure over HTTPS
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,        #only sent over HTTPS
    SESSION_COOKIE_SAMESITE="Lax"      #prevents CSRF in many cases
)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY not set")

@app.route("/", methods=["GET","POST"])
def index():
    answer  = sources = error = None

    if request.method == "POST":
        #clear existing pdf and files
        if "clear" in request.form:
            session.pop("upload_id",  None)
            session.pop("pdf_name",   None)
            for fn in os.listdir(DATA_PATH):
                os.remove(os.path.join(DATA_PATH, fn))
            return redirect(url_for("index"))

        #handle new upload
        pdf = request.files.get("pdf")
        if pdf and pdf.filename:
            upload_id    = str(uuid.uuid4())
            original_name = pdf.filename

            #clear old pdfs before saving the new one
            for fn in os.listdir(DATA_PATH):
                os.remove(os.path.join(DATA_PATH, fn))

            #save the uploaded file
            pdf_path = os.path.join(DATA_PATH, f"{upload_id}.pdf")
            pdf.save(pdf_path)

            #index it once in its own folder
            chroma_folder = os.path.join(BASE_CHROMA, upload_id)
            os.makedirs(chroma_folder, exist_ok=True)
            docs   = load_documents(DATA_PATH)
            chunks = split_documents(docs)
            add_to_chroma(chunks, chroma_folder)

            #store both the internal id and the display name
            session["upload_id"] = upload_id
            session["pdf_name"]  = original_name

            return redirect(url_for("index"))

        #handle question against existing upload
        upload_id = session.get("upload_id")
        if not upload_id:
            error = "No PDF uploaded. Please upload one first."
        else:
            q = request.form.get("question", "").strip()
            if not q:
                error = "Please enter a question."
            else:
                chroma_folder = os.path.join(BASE_CHROMA, upload_id)
                answer, sources = query_rag(q, chroma_folder)
                    #translate raw chunk-IDs into “filename – page X”
    display_sources = []
    pdf_name = session.get("pdf_name", "document")
    for src in sources or []:
        try:
            #src looks like "data\\<uuid>.pdf:0:2"
            path_part, page_str, _chunk = src.split(":")
            page_num = int(page_str) + 1  # convert zero-based to human page
            display_sources.append(f"{pdf_name} – page {page_num}")
        except Exception:
            #fallback to the raw id if parsing fails
            display_sources.append(src)


    #get values to pass into template
    upload_id = session.get("upload_id")
    display_name = session.get("pdf_name") if upload_id else None

    return render_template(
        "index.html",
        answer=answer,
        sources=sources,             #optional no need #doesnt break it
        display_sources=display_sources,
        error=error,
        upload_id=upload_id,
        pdf_name=display_name
    )

if __name__ == "__main__":
    os.makedirs(DATA_PATH,   exist_ok=True)
    os.makedirs(BASE_CHROMA, exist_ok=True)
    app.run(debug=True)
