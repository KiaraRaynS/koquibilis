from flask import Flask, render_template, request, redirect, url_for
import os
import json
import boto3

app = Flask(__name__)


@app.route('/accounts/profile/')
def account():
    return render_template('profileview.html')


@app.route('/sign_s3/')
def sign_s3():
    S3_BUCKET = os.environ.get('S3_BUCKET_NAME')

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = boto3.client('s3')

    presigned_post = s3.generate_presigned_post(
              Bucket=S3_BUCKET,
              Key=file_name,
              Fields={"acl": "public-read", "Content-Type": file_type},
              Conditions=[
                            {"acl": "public-read"},
                            {"Content-Type": file_type}
                          ],
              ExpiresIn=3600
            )

    return json.dumps({
      'data': presigned_post,
      'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
                    })

    @app.route("/submit_form/", methods=["POST"])
    def submit_form():
        avatar_url = request.form["icon-url"]

        update_account(avatar_url)

        return redirect(url_for('profile'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
