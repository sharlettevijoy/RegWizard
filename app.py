from flask import Flask, render_template, request
from agent import run_pipeline_sync, REGULATIONS

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    reg_id = request.args.get("reg_id")
    regulation_text = ""
    mapped_policies = []
    error = None

    if reg_id:
        try:
            regulation_text, mapped_policies = run_pipeline_sync(reg_id)
        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        regulations=REGULATIONS.keys(),
        selected_reg=reg_id,
        regulation_text=regulation_text,
        mapped_policies=mapped_policies,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)