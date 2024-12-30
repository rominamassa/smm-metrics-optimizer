from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static')  # Explicitly set the static folder

@app.route('/', methods=['GET', 'POST'])
def index():
    organic_results = None
    paid_results = None
    form_data = {}

    if request.method == 'POST':
        form_data = request.form.to_dict()

        # Handle Organic Metrics form
        if 'reach' in request.form:
            try:
                # Retrieve inputs, ignoring blank fields
                reach = request.form.get('reach')
                impressions = request.form.get('impressions')
                followers = request.form.get('followers')
                likes = request.form.get('likes')
                comments = request.form.get('comments')
                shares = request.form.get('shares')
                saves = request.form.get('saves')
                link_clicks = request.form.get('link_clicks')

                # Convert only filled fields to floats, skip blanks
                reach = float(reach) if reach else None
                impressions = float(impressions) if impressions else None
                followers = float(followers) if followers else None
                likes = float(likes) if likes else 0
                comments = float(comments) if comments else 0
                shares = float(shares) if shares else 0
                saves = float(saves) if saves else 0
                link_clicks = float(link_clicks) if link_clicks else 0

                # Engagement metrics
                total_engagements = likes + comments + shares + saves + link_clicks
                organic_results = {
                    'engagement_by_reach': round((total_engagements / reach) * 100, 2) if reach else None,
                    'engagement_by_impressions': round((total_engagements / impressions) * 100, 2) if impressions else None,
                    'engagement_by_followers': round((total_engagements / followers) * 100, 2) if followers else None,
                    'discovery_rate': round((shares / reach) * 100, 2) if reach else None,
                    'click_rate': round((link_clicks / reach) * 100, 2) if reach else None,
                }
                print("Organic Results:", organic_results)  # Debugging output
            except Exception as e:
                print("Error calculating organic metrics:", e)

        # Handle Paid Metrics form
        if 'impressions_paid' in request.form:
            try:
                # Retrieve inputs, ignoring blank fields
                impressions = request.form.get('impressions_paid')
                clicks = request.form.get('clicks')
                results = request.form.get('results')
                spend = request.form.get('spend')

                # Convert only filled fields to floats, skip blanks
                impressions = float(impressions) if impressions else None
                clicks = float(clicks) if clicks else None
                results = float(results) if results else None
                spend = float(spend) if spend else None

                # Paid metrics
                paid_results = {
                    'ctr': round((clicks / impressions) * 100, 2) if impressions and clicks else None,
                    'cpc': round(spend / clicks, 2) if spend and clicks else None,
                    'cpr': round(spend / results, 2) if spend and results else None,
                }
                print("Paid Results:", paid_results)  # Debugging output
            except Exception as e:
                print("Error calculating paid metrics:", e)

    # Render the same page with results and form data
    return render_template('index.html', organic_results=organic_results, paid_results=paid_results, form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
