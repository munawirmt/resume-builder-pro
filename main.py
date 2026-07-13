from flask import Flask, render_template_string, request
import base64

app = Flask(__name__)

# ഡാർക്ക് മോഡ് സ്വിച്ച് ഉൾപ്പെടുത്തിയ പുതിയ UI ഫോം
html_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Resume Builder Pro</title>
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            --card-bg: white;
            --text-color: #333;
            --input-border: #ddd;
            --input-bg: #fff;
            --title-color: #1e3c72;
            --label-color: #555;
        }
        
        /* ഡാർക്ക് തീം സ്റ്റൈലുകൾ */
        [data-theme="dark"] {
            --bg-gradient: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            --card-bg: #1e272e;
            --text-color: #f5f6fa;
            --input-border: #485460;
            --input-bg: #2f3640;
            --title-color: #00d2d3;
            --label-color: #dcdde1;
        }

        body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; background: var(--bg-gradient); min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--text-color); transition: 0.3s; }
        .container { max-width: 650px; width: 100%; background: var(--card-bg); padding: 30px; border-radius: 15px; box-shadow: 0px 10px 25px rgba(0,0,0,0.3); box-sizing: border-box; position: relative; transition: 0.3s; }
        
        /* ഡാർക്ക് മോഡ് ടോഗിൾ ബട്ടൺ */
        .theme-switch { position: absolute; top: 20px; right: 20px; background: #74b9ff; color: #fff; border: none; padding: 8px 12px; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 12px; }
        [data-theme="dark"] .theme-switch { background: #f1c40f; color: #2c3e50; }

        h2 { text-align: center; color: var(--title-color); margin-bottom: 5px; font-size: 26px; font-weight: bold; }
        p.subtitle { text-align: center; color: #888; margin-bottom: 25px; font-size: 14px; }
        .section-title { font-size: 16px; font-weight: bold; color: var(--title-color); border-bottom: 2px solid var(--title-color); padding-bottom: 5px; margin-top: 20px; margin-bottom: 10px; }
        input, textarea, select { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid var(--input-border); background: var(--input-bg); color: var(--text-color); border-radius: 8px; box-sizing: border-box; font-size: 14px; }
        input[type="file"] { background: var(--input-bg); padding: 10px; border: 1px dashed var(--title-color); cursor: pointer; }
        .template-option { display: flex; gap: 15px; margin: 10px 0; }
        .template-option label { font-size: 14px; font-weight: bold; color: var(--text-color); cursor: pointer; }
        button.submit-btn { width: 100%; background: linear-gradient(to right, #1e3c72, #2a5298); color: white; padding: 15px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; margin-top: 25px; }
        .app-footer { margin-top: 20px; text-align: center; color: #ffffff; font-size: 13px; opacity: 0.9; line-height: 1.5; }
        .app-footer a { color: #fff; text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <!-- ഡാർക്ക് മോഡ് മാറ്റാനുള്ള ബട്ടൺ -->
        <button class="theme-switch" id="toggleTheme" type="button">🌙 DARK MODE</button>
        
        <h2>Resume Builder Premium</h2>
        <p class="subtitle">Generate High-Quality Executive Resumes</p>
        
        <form action="/view_resume" method="post" enctype="multipart/form-data">
            <div class="section-title">Choose Resume Template</div>
            <div class="template-option">
                <input type="radio" id="temp1" name="template" value="modern" checked style="width:auto; margin:0;">
                <label for="temp1">🔵 Modern Blue</label>
                
                <input type="radio" id="temp2" name="template" value="elegant" style="width:auto; margin:0;">
                <label for="temp2">🟢 Elegant Green</label>
                
                <input type="radio" id="temp3" name="template" value="minimal" style="width:auto; margin:0;">
                <label for="temp3">⚫ Minimal Black</label>
            </div>

            <div class="section-title">Personal Details</div>
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="text" name="job_title" placeholder="Professional Title" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="text" name="phone" placeholder="Phone Number" required>
            <input type="text" name="linkedin" placeholder="LinkedIn Profile Link (Optional)">
            <input type="text" name="github" placeholder="GitHub Profile Link (Optional)">

            <label style="font-size:13px; color:var(--label-color); font-weight:bold; margin-top:5px; display:block;">Upload Profile Photo:</label>
            <input type="file" name="photo" accept="image/*">

            <div class="section-title">Professional Summary</div>
            <textarea name="summary" placeholder="Write a short summary about your career goals..." rows="3" required></textarea>

            <div class="section-title">Work Experience</div>
            <textarea name="experience" placeholder="Job Title - Company Name (Year)" rows="4" required></textarea>

            <div class="section-title">Education</div>
            <textarea name="education" placeholder="Degree Name - College/University (Year)" rows="3" required></textarea>

            <div class="section-title">Projects & Links</div>
            <textarea name="projects" placeholder="Project Name - Brief details" rows="3" required></textarea>
            <input type="text" name="project_link" placeholder="Project Link">

            <div class="section-title">Skills & Languages</div>
            <input type="text" name="skills" placeholder="Skills" required>
            <input type="text" name="languages" placeholder="Languages">

            <div class="section-title">Certifications</div>
            <input type="file" name="cert_file" accept="image/*">

            <button type="submit" class="submit-btn">GENERATE PREMIUM RESUME</button>
        </form>
    </div>

    <div class="app-footer">
        © 2026 Resume Builder Pro. All Rights Reserved.<br>
        <strong>Built by MUNAWIR MT</strong> | Support: <a href="mailto:munawirmt002@gmail.com">munawirmt002@gmail.com</a>
    </div>

    <!-- തീം മാറാനുള്ള ജാവാസ്ക്രിപ്റ്റ് ലോജിക് -->
    <script>
        const toggleBtn = document.getElementById('toggleTheme');
        toggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'light');
                toggleBtn.textContent = '🌙 DARK MODE';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                toggleBtn.textContent = '☀️ LIGHT MODE';
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_form)
@app.route('/view_resume', methods=['POST'])
def view_resume():
    name = request.form['name']
    job_title = request.form['job_title']
    email = request.form['email']
    phone = request.form['phone']
    linkedin = request.form.get('linkedin', '')
    github = request.form.get('github', '')
    summary = request.form['summary']
    education = request.form['education']
    experience = request.form['experience']
    projects = request.form['projects']
    project_link = request.form.get('project_link', '')
    skills = request.form['skills']
    languages = request.form.get('languages', '')
    selected_template = request.form.get('template', 'modern')

    photo_file = request.files.get('photo')
    img_html = ""
    if photo_file and photo_file.filename != '':
        encoded_img = base64.b64encode(photo_file.read()).decode('utf-8')
        img_html = f'<img src="data:image/png;base64,{encoded_img}" class="profile-img">'

    cert_file = request.files.get('cert_file')
    cert_html = ""
    if cert_file and cert_file.filename != '':
        encoded_cert = base64.b64encode(cert_file.read()).decode('utf-8')
        cert_html = f'<div class="section page-break"><div class="section-title">Attached Certification</div><img src="data:image/png;base64,{encoded_cert}" class="cert-img"></div>'

    theme_color = "#1e3c72"
    if selected_template == "elegant":
        theme_color = "#1b4d3e"
    elif selected_template == "minimal":
        theme_color = "#222222"

    resume_design = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{name}_Resume</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #333; margin: 0; padding: 40px; background-color: #fff; min-height: 90vh; }}
            .header-container {{ display: flex; justify-content: space-between; align-items: center; background-color: {theme_color}; color: white; padding: 30px; border-radius: 8px; margin-bottom: 25px; }}
            .header-text h1 {{ margin: 0; font-size: 32px; letter-spacing: 1px; }}
            .header-text p {{ margin: 5px 0 0 0; font-size: 16px; color: #dae2f8; font-weight: bold; }}
            .profile-img {{ width: 100px; height: 110px; border-radius: 6px; border: 3px solid white; object-fit: cover; }}
            .contact-info {{ background-color: #f4f6f9; padding: 12px; border-radius: 6px; font-size: 13px; margin-bottom: 25px; color: #555; }}
            .section {{ margin-bottom: 25px; }}
            .section-title {{ font-size: 16px; font-weight: bold; color: {theme_color}; border-bottom: 2px solid {theme_color}; padding-bottom: 5px; margin-bottom: 12px; text-transform: uppercase; }}
            .content {{ font-size: 14px; line-height: 1.6; white-space: pre-line; color: #444; }}
            .project-url {{ font-size: 13px; color: {theme_color}; font-weight: bold; text-decoration: none; }}
            .cert-img {{ max-width: 100%; height: auto; border: 1px solid #ccc; margin-top: 10px; }}
            
            .btn-container {{ display: flex; gap: 15px; margin-bottom: 20px; }}
            .btn-print {{ background-color: #28a745; color: white; padding: 12px 25px; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }}
            .btn-share {{ background-color: #25D366; color: white; padding: 12px 25px; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 8px; text-decoration: none; }}
            
            .pdf-footer {{ text-align: center; font-size: 10px; color: #999; margin-top: 50px; border-top: 1px dashed #eee; padding-top: 10px; }}
            @media print {{
                .btn-container {{ display: none; }}
                body {{ padding: 0; }}
                .page-break {{ page-break-before: always; }}
            }}
        </style>
    </head>
    <body>
        <div class="btn-container">
            <button class="btn-print" onclick="window.print()">📥 DOWNLOAD AS PDF</button>
            <a class="btn-share" href="https://wa.me/?text=I have generated my professional resume using Resume Builder Pro app! Please check it out." target="_blank">💬 SHARE ON WHATSAPP</a>
        </div>

        <div class="header-container">
            <div class="header-text">
                <h1>{name.upper()}</h1>
                <p>{job_title.upper()}</p>
            </div>
            {img_html}
        </div>

        <div class="contact-info">
            <strong>Email:</strong> {email} &nbsp;|&nbsp; 
            <strong>Phone:</strong> {phone}
            {f" &nbsp;|&nbsp; <strong>LinkedIn:</strong> {linkedin}" if linkedin else ""}
            {f" &nbsp;|&nbsp; <strong>GitHub:</strong> {github}" if github else ""}
        </div>

        <div class="section">
            <div class="section-title">Professional Summary</div>
            <div class="content">{summary}</div>
        </div>

        <div class="section">
            <div class="section-title">Work Experience</div>
            <div class="content">{experience}</div>
        </div>

        <div class="section">
            <div class="section-title">Education</div>
            <div class="content">{education}</div>
        </div>

        <div class="section">
            <div class="section-title">Projects</div>
            <div class="content">{projects}</div>
            {f'<a href="{project_link}" class="project-url" target="_blank">🔗 Project Link: {project_link}</a>' if project_link else ""}
        </div>

        <div class="section">
            <div class="section-title">Key Skills</div>
            <div class="content">{skills}</div>
        </div>

        {f'<div class="section"> <div class="section-title">Languages</div> <div class="content">{languages}</div> </div>' if languages else ""}
        
        {cert_html}

        <div class="pdf-footer">
            Generated via Resume Builder Pro | Built by Munawir MT (munawirmt002@gmail.com)
        </div>
    </body>
    </html>
    """
    return render_template_string(resume_design)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
