# from flask import Flask, render_template, request, jsonify
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# from calculations import calculate_metrics, calculate_single_metric

# app = Flask(__name__)

# chatbot = ChatBot("ProjectBot")
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train("chatterbot.corpus.english")

# projects = []
# roi = []

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     global current_project
#     user_input = request.json['message']

    
#     if user_input.lower().startswith("compare projects"):
#         if not projects:
#             return jsonify({"reply": "❌ No projects entered yet. Please add some first."})
        
#         table, summary = calculate_metrics(projects)
#         full_reply = f"📊 <b>Project Comparison:</b><br><pre>{table}</pre><br>{summary}"
#         return jsonify({"reply": full_reply})

#     if user_input.lower().startswith("add project"):
#         try:
#             parts = user_input[len("add project "):]
#             name_part, cost_part, rate_part, cf_part = parts.split(",")
#             name = name_part.strip()
#             cost = float(cost_part.split("=")[1])
#             rate = float(rate_part.split("=")[1])
#             cf_raw = cf_part.split("=")[1].strip("[] ")
#             cash_flows = list(map(float, cf_raw.split()))
#             projects.append({
#                 "name": name,
#                 "initial_cost": cost,
#                 "discount_rate": rate,
#                 "cash_flows": cash_flows
#             })
#             return jsonify({"reply": f"✅ Project '<b>{name}</b>' added successfully."})
#         except Exception as e:
#             return jsonify({"reply": f"❌ Failed to add project. Make sure format is correct. Error: {str(e)}"})
        
#     elif user_input.startswith("calculate"):
#         if not current_project:
#             return jsonify({"reply": "❌ Please add a project first using 'add project' command."})
#         try:
#             metric = user_input.replace("calculate", "").strip()
#             result = calculate_single_metric(current_project, metric)
#             return jsonify({"reply": f"📊 <b>{metric.upper()}:</b> {result}"})
#         except Exception as e:
#             return jsonify({"reply": f"❌ Error calculating {metric}. {str(e)}"})   
#     # if user_input.lower().startswith("calculate"):
#     #     return jsonify({"reply": "🤖 I can help you calculate NPV, IRR, ROI, Payback or BCR after you add a project. Please enter 'calculate ROI' or 'Calculate NPV' and so on to calculate "})
    
#     # if user_input.lower().startswith("calculate ROI"):
#     #     return jsonify({"reply": "🤖 Please add project name, initial investment and annual cashflows like add project_name, initial_investment, Annual cashflow like [3000 3000 3000 ...]"})
    
#     # if user_input.lower().startswith("add"):
#     #     try:
#     #         parts = user_input[len("add "):]
#     #         name_part, cost_part, cf_part = parts.split(",")
#     #         name = name_part.strip()
#     #         cost = float(cost_part.split("=")[1])
#     #         cf_raw = cf_part.split("=")[1].strip("[] ")
#     #         cash_flows = list(map(float, cf_raw.split()))
#     #         roi.append({
#     #             "name": name,
#     #             "initial_cost": cost,
#     #             "cash_flows": cash_flows
#     #         })
#     #         return jsonify({"reply": f"✅ Project '<b>{name}</b>' added successfully."})
#     #     except Exception as e:
#     #         return jsonify({"reply": f"❌ Failed to add project. Make sure format is correct. Error: {str(e)}"})

    

#     response = chatbot.get_response(user_input)
#     return jsonify({"reply": str(response)})



# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template, request, jsonify
from calculations import calculate_single_metric

app = Flask(__name__)

current_project = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global current_project
    user_input = request.json['message'].strip().lower()

    if user_input.startswith("add project"):
        try:
            parts = user_input[len("add project "):]
            name_part, cost_part, rate_part, cf_part = parts.split(",")
            name = name_part.split("=")[1].strip()
            cost = float(cost_part.split("=")[1])
            rate = float(rate_part.split("=")[1])
            cf_raw = cf_part.split("=")[1].strip("[] ")
            cash_flows = list(map(float, cf_raw.split()))
            current_project = {
                "name": name,
                "initial_cost": cost,
                "discount_rate": rate,
                "cash_flows": cash_flows
            }
            return jsonify({"reply": f"✅ Project '<b>{name}</b>' added successfully."})
        except Exception as e:
            return jsonify({"reply": f"❌ Failed to add project. Error: {str(e)}"})

    elif user_input.startswith("calculate"):
        if not current_project:
            return jsonify({"reply": "❌ Please add a project First\n To add project, use the format for example: 'add project name=A, initial investment=10000, discount rate=10, annual cash flow=[2000 3000 4000 ..]'\nThen type 'Calculate ROI' or 'Calculate NPV' so on"})
        try:
            metric = user_input.replace("calculate", "").strip()
            result = calculate_single_metric(current_project, metric)
            return jsonify({"reply": f"📊 <b>{metric.upper()}:</b> {result}"})
        except Exception as e:
            return jsonify({"reply": f"❌ Error calculating {metric}. {str(e)}"})

    return jsonify({"reply": "🤖 I can help you calculate NPV, IRR, ROI, Payback or BCR after you add a project."})

if __name__ == "__main__":
    app.run(debug=True)

