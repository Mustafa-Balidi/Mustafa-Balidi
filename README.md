<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mustafa balidi · interactive portfolio</title>
    <!-- Font Awesome 6 (free) for crisp icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Google Fonts: Inter & space for fun -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #f1f4f8;
            font-family: 'Inter', sans-serif;
            color: #1e293b;
            line-height: 1.5;
            padding: 2rem 1.5rem;
        }

        .container {
            max-width: 1300px;
            margin: 0 auto;
        }

        /* card / glassmorphism style */
        .card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 2.5rem;
            box-shadow: 0 20px 40px -10px rgba(0,20,40,0.2), 0 8px 20px rgba(0,0,0,0.06);
            padding: 2.5rem 2.2rem;
            border: 1px solid rgba(255,255,255,0.5);
            transition: transform 0.2s ease;
        }

        .card:hover {
            transform: scale(1.005);
        }

        /* header section — exactly like original markdown but with UI flair */
        .hero {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 2.5rem;
            margin-bottom: 3rem;
        }

        .hero-content {
            flex: 1 1 300px;
        }

        .hero-greeting {
            font-size: 2.8rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }

        .hero-greeting img {
            width: 48px;
            height: 48px;
            vertical-align: middle;
            margin-left: 8px;
            transform: translateY(-2px);
        }

        .hero-title {
            font-size: 1.9rem;
            font-weight: 600;
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0.75rem 0 0.5rem;
        }

        .hero-gif {
            flex: 0 0 400px;
            text-align: center;
        }

        .hero-gif img {
            max-width: 100%;
            width: 400px;
            border-radius: 32px;
            box-shadow: 0 30px 30px -15px rgba(0,0,0,0.25);
            background: #ffffff40;
            padding: 8px 0 0;
            transition: 0.3s;
        }

        /* tech stack grid */
        .section-title {
            font-size: 2rem;
            font-weight: 650;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 2.2rem 0 1.8rem;
        }

        .section-title i {
            font-size: 2.1rem;
            color: #2563eb;
        }

        .icons-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem 1.2rem;
            align-items: center;
        }

        .icons-grid a {
            display: inline-flex;
            background: white;
            padding: 0.9rem 1.2rem;
            border-radius: 50px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.02);
            border: 1px solid #e9eef3;
            transition: all 0.2s;
        }

        .icons-grid a:hover {
            border-color: #2563eb40;
            box-shadow: 0 12px 20px -12px #2563eb60;
            transform: translateY(-3px);
        }

        .icons-grid img {
            width: 42px;
            height: 42px;
            object-fit: contain;
        }

        /* about me — list style fresh */
        .about-list {
            list-style: none;
            font-size: 1.2rem;
        }

        .about-list li {
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 16px;
            border-bottom: 1px dashed #cbd5e1;
            padding-bottom: 0.7rem;
        }

        .about-list li:last-child {
            border-bottom: none;
        }

        .bullet-icon {
            font-size: 2rem;
            min-width: 2.5rem;
            text-align: center;
        }

        .about-text {
            font-weight: 500;
        }

        .highlight {
            background: #e2e8f0;
            padding: 0.2rem 0.8rem;
            border-radius: 40px;
            font-weight: 600;
            color: #0f172a;
        }

        /* social badges row */
        .social-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin-top: 2rem;
            align-items: center;
        }

        .social-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: #0f172a;
            color: white;
            padding: 0.8rem 1.8rem;
            border-radius: 60px;
            font-weight: 600;
            font-size: 1.1rem;
            text-decoration: none;
            transition: 0.2s;
            box-shadow: 0 5px 10px rgba(0,0,0,0.1);
            border: 1px solid #ffffff30;
        }

        .social-badge i {
            font-size: 1.6rem;
        }

        .social-badge:hover {
            background: #1e293b;
            transform: translateY(-3px);
        }

        .linkedin { background: #0A66C2; }
        .twitter { background: #1D9BF0; }
        .facebook { background: #1877F2; }
        .instagram { background: #D7008A; }
        .website { background: #8b5cf6; }

        /* footer extra */
        .fun-note {
            margin-top: 3rem;
            font-size: 1.1rem;
            text-align: center;
            opacity: 0.8;
        }

        hr {
            border: none;
            border-top: 2px dotted #b9c9da;
            margin: 2rem 0 1rem;
        }
        /* small adjustment */
        @media (max-width: 800px) {
            .hero {
                flex-direction: column-reverse;
                text-align: center;
            }
            .hero-greeting img { width: 40px; height: 40px; }
            .section-title { justify-content: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- main card (figma-like frame) -->
        <div class="card">

            <!-- === H2 SECTION exactly like original: "Hi there! ... I'm Mustafa balidi ..." -->
            <div class="hero">
                <div class="hero-content">
                    <h2 style="font-size: 0; line-height: 0; margin: 0; visibility: hidden;">Hidden original anchor</h2>
                    <!-- visible replica of <h2 align="left"> content -->
                    <div class="hero-greeting">
                        Hi there! 
                        <img src="https://user-images.githubusercontent.com/42378118/110234147-e3259600-7f4e-11eb-95be-0c4047144dea.gif" alt="waving hand" width="48" style="display: inline;">
                    </div>
                    <div class="hero-title">
                        I'm Mustafa balidi, Frontend And UI/UX Designer 💻
                    </div>
                    <!-- additional text from original h2 (the <br> are handled) -->
                    <p style="font-size: 1.1rem; margin-top: 8px; color: #334155;">&nbsp;</p> <!-- spacer -->
                </div>
                <div class="hero-gif">
                    <img src="https://media.giphy.com/media/SWoSkN6DxTszqIKEqv/giphy.gif" alt="Coder GIF">
                </div>
            </div>

            <!-- === Technologies and Tools I use: (h2) -->
            <div class="section-title">
                <i class="fas fa-hammer"></i>
                <span>Technologies and Tools I use:</span>
            </div>

            <!-- icon grid — exactly same order as markdown, with vector badges from zone or devicon -->
            <div class="icons-grid">
                <!-- HTML5 -->
                <a href="#" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5"></a>
                <!-- CSS3 -->
                <a href="#" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3"></a>
                <!-- SASS -->
                <a href="#" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sass/sass-original.svg" alt="sass"></a>
                <!-- JavaScript -->
                <a href="#" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript"></a>
                <!-- React -->
                <a href="#" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/react/react-original-wordmark.svg" alt="react"></a>
                <!-- Gatsby -->
                <a href="#" target="_blank"><img src="https://www.vectorlogo.zone/logos/gatsbyjs/gatsbyjs-icon.svg" alt="gatsby"></a>
                <!-- Node.js -->
                <a href="#" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original-wordmark.svg" alt="nodejs"></a>
                <!-- Express -->
                <a href="#" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/express/express-original-wordmark.svg" alt="express"></a>
                <!-- MongoDB -->
                <a href="#" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original-wordmark.svg" alt="mongodb"></a>
                <!-- Postman -->
                <a href="#" target="_blank"><img src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="postman"></a>
                <!-- Git -->
                <a href="#" target="_blank"><img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git"></a>
                <!-- Azure -->
                <a href="#" target="_blank"><img src="https://www.vectorlogo.zone/logos/microsoft_azure/microsoft_azure-icon.svg" alt="azure"></a>
                <!-- Google Cloud -->
                <a href="#" target="_blank"><img src="https://www.vectorlogo.zone/logos/google_cloud/google_cloud-icon.svg" alt="google cloud"></a>
                <!-- Firebase -->
                <a href="#" target="_blank"><img src="https://www.vectorlogo.zone/logos/firebase/firebase-icon.svg" alt="firebase"></a>
            </div>

            <!-- === About Me section -->
            <div class="section-title" style="margin-top: 3rem;">
                <i class="fas fa-user-astronaut"></i>
                <span>👨🏻‍💻 About Me:</span>
            </div>

            <ul class="about-list">
                <li><span class="bullet-icon">💻</span><span class="about-text">I'm a Fullstack Developer, currently exploring Web3 Space</span></li>
                <li><span class="bullet-icon">⏳</span><span class="about-text">Exploring Google Cloud & Microsoft Azure</span></li>
                <li><span class="bullet-icon">🚀</span><span class="about-text">Always ready to collaborate for Dev Experiments</span></li>
                <li><span class="bullet-icon">👨‍🔧</span><span class="about-text">Former Project Lead Intern at GirlScript Foundation</span></li>
                <li><span class="bullet-icon">🎯</span><span class="about-text">Life Hack: "Explore 🔥 and Explode 💣 with knowledge"</span></li>
                <li><span class="bullet-icon">🏆</span><span class="about-text">Grand Finalist of "Smart India Hackathon 2019" - Software Edition</span></li>
                <li><span class="bullet-icon">⚡</span><span class="about-text">Fun fact: I love to attend Meetups for learning & Conferences for Networking</span></li>
            </ul>

            <!-- === heart / Let's get connected: exactly with social badges -->
            <div class="section-title" style="margin-top: 2.8rem;">
                <i class="fas fa-heart" style="color: #dc2626;"></i>
                <span>Let's get connected:</span>
            </div>

            <div class="social-row">
                <!-- linkedin badge (matching username but placeholder uses #) 
                     original markdown showed sivramshastri, but we respect the name Mustafa? 
                     we'll use placeholder links but keep username pattern for design -->
                <a href="https://www.linkedin.com/in/sivramshastri" class="social-badge linkedin" target="_blank"><i class="fab fa-linkedin-in"></i> sivramshastri</a>
                
                <!-- twitter -->
                <a href="https://twitter.com/prince_shivaram" class="social-badge twitter" target="_blank"><i class="fab fa-twitter"></i> @prince_shivaram</a>
                
                <!-- facebook -->
                <a href="https://www.facebook.com/jonnalagadda.shivaram" class="social-badge facebook" target="_blank"><i class="fab fa-facebook-f"></i> jonnalagadda.shivaram</a>
                
                <!-- instagram -->
                <a href="https://www.instagram.com/itz.me____p.r.i.n.c.e_____/" class="social-badge instagram" target="_blank"><i class="fab fa-instagram"></i> itz.me____p.r.i.n.c.e_____</a>
                
                <!-- personal site -->
                <a href="https://sivram.tech/" class="social-badge website" target="_blank"><i class="fas fa-globe"></i> sivram.tech</a>
            </div>

            <!-- Additional raw paragraph from markdown that includes extra linkedin badge? 
                 In original there is a second [Linkedin Badge] after instagram. 
                 we will replicate as inline small note with style but keep consistent  -->
            <div style="display: flex; flex-wrap: wrap; gap: 0.8rem; margin-top: 1.5rem; align-items: center;">
                <!-- duplicate badge: LinkedIn (same) but using light style as in markdown extra line? 
                It was [Linkedin Badge ... Sivram.tech] — we integrate it creatively -->
                <span style="background: #f0f4fa; padding: 0.5rem 1.2rem; border-radius: 40px; font-size: 1rem;">
                    <i class="fab fa-linkedin" style="color:#0A66C2;"></i> 
                    <a href="https://sivram.tech/" style="text-decoration:none; color:#1e293b; font-weight:600;">Sivram.tech</a>
                </span>
                <!-- also add the 'Linkedin Badge' variant from end of original -->
                <span style="background: #f0f4fa; padding: 0.5rem 1.2rem; border-radius: 40px;">
                    <i class="fab fa-linkedin" style="color:#0A66C2;"></i> 
                    <a href="https://www.linkedin.com/in/sivramshastri" style="text-decoration:none; font-weight:600;">LinkedIn (alt)</a>
                </span>
                <!-- We'll also place a note that the profile originally includes both, but it's fine -->
            </div>

            <!-- small caption to match markdown extra text: 
                 "this file edit tool to figma and html and css and sass and js and react.js" 
                 must be included exactly as last line. -->
            <hr>
            <div class="fun-note">
                <i class="fa-regular fa-pen-to-square"></i> this file edit tool to figma and html and css and sass and js and react.js
            </div>

            <!-- also include the original closing line, no extra. but we need final line with hi there-->

        </div> <!-- end main card -->

        <!-- tiny signature to keep original spirit -->
        <p style="margin-top: 1.5rem; text-align: right; opacity: 0.6; font-size: 0.95rem;">
            <i class="fa-regular fa-face-smile"></i> Mustafa balidi · interactive edition
        </p>
    </div>

    <!-- small tooltip to ensure all links open properly (some are placeholders) but we preserve them for design -->
</body>
</html>
