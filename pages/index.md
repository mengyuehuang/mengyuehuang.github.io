---
layout: home
permalink: /
title: Mengyue Huang — Data Scientist
description: Data scientist and ML engineer building reliable models, thoughtful analytics, and useful data products.
---

<a class="skip-link" href="#work">Skip to selected work</a>

<header class="site-header" data-header>
  <a class="wordmark" href="#top" aria-label="Mengyue Huang, home">MH<span>.</span></a>
  <nav aria-label="Primary navigation">
    <a href="#work">Work</a>
    <a href="#experience">Experience</a>
    <a href="{{ '/blog/' | relative_url }}">Blog</a>
    <a href="#about">About</a>
  </nav>
  <a class="header-cta" href="mailto:{{ site.author.email }}">Open to roles <span>↗</span></a>
</header>

<main id="top">
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-copy reveal">
      <p class="eyebrow"><span class="status-dot"></span> Open to data science &amp; ML opportunities</p>
      <h1 id="hero-title">I turn messy data into <em>clear decisions.</em></h1>
      <p class="hero-intro">I’m Mengyue, a data scientist at Penn working across machine learning, analytics, and data products—especially where rigorous modeling meets a genuinely useful interface.</p>
      <div class="hero-actions">
        <a class="button button-primary" href="#work">Explore my work <span>↓</span></a>
        <a class="text-link" href="mailto:{{ site.author.email }}">{{ site.author.email }} <span>↗</span></a>
      </div>
      <div class="hero-meta" aria-label="Quick facts">
        <div><strong>MSE</strong><span>Data Science · UPenn ’26</span></div>
        <div><strong>3.80</strong><span>Graduate GPA</span></div>
        <div><strong>Philadelphia</strong><span>Based in Pennsylvania</span></div>
      </div>
    </div>
    <div class="hero-visual reveal" data-delay="1">
      <div class="image-frame">
        <img src="{{ '/assets/pngs/cover.jpg' | relative_url }}" alt="Mengyue snowboarding on a winter mountain" fetchpriority="high">
        <p class="image-note">Off the clock: usually outside, occasionally upright.</p>
      </div>
      <div class="floating-card">
        <span>Currently exploring</span>
        <strong>Reliable ML systems</strong>
        <small>from signal to story</small>
      </div>
    </div>
  </section>

  <section class="marquee" aria-label="Core capabilities">
    <div>Python <span>✦</span> Pandas <span>✦</span> scikit-learn <span>✦</span> PyTorch <span>✦</span> SQL <span>✦</span> R <span>✦</span> XGBoost <span>✦</span> LightGBM <span>✦</span> Random Forest <span>✦</span> Regression <span>✦</span> Neural Networks <span>✦</span> SVM <span>✦</span> Gaussian Mixture Models <span>✦</span> Clustering <span>✦</span> PCA <span>✦</span> t-SNE <span>✦</span> Time Series <span>✦</span> A/B Testing <span>✦</span> Causal Inference <span>✦</span> Data Wrangling <span>✦</span> Database Management <span>✦</span> Visualization <span>✦</span> Python <span>✦</span> Pandas <span>✦</span> scikit-learn <span>✦</span> PyTorch <span>✦</span> SQL <span>✦</span> R <span>✦</span> XGBoost <span>✦</span> LightGBM <span>✦</span> Random Forest <span>✦</span> Regression <span>✦</span> Neural Networks <span>✦</span> SVM <span>✦</span> Gaussian Mixture Models <span>✦</span> Clustering <span>✦</span> PCA <span>✦</span> t-SNE <span>✦</span> Time Series <span>✦</span> A/B Testing <span>✦</span> Causal Inference <span>✦</span> Data Wrangling <span>✦</span> Database Management <span>✦</span> Visualization <span>✦</span></div>
  </section>

  <section class="work section" id="work" aria-labelledby="work-title">
    <div class="section-heading reveal">
      <div><p class="eyebrow">01 / Selected work</p><h2 id="work-title">Projects with a point of view.</h2></div>
      <p>My research in wearable and EEG signals shaped how I approach applied ML: start with data quality, validate carefully, and translate results for people.</p>
    </div>

    <div class="project-filters reveal" role="group" aria-label="Filter projects">
      <button class="active" type="button" data-filter="all">All</button>
      <button type="button" data-filter="ml">Machine Learning</button>
      <button type="button" data-filter="analytics">Analytics</button>
      <button type="button" data-filter="research">Research</button>
    </div>

    <div class="project-grid">
      <a class="project-card project-featured reveal" data-category="ml" href="{{ '/projects/1-hotel-bookings' | relative_url }}">
        <div class="project-image project-image-hotel"><div class="mini-chart"><i></i><i></i><i></i><i></i><i></i></div><span>IHG</span><small>cancellation prediction</small></div>
        <div class="project-body"><p class="project-index">01 · Predictive modeling</p><h3>IHG hotel cancellation analysis</h3><p>Led an end-to-end workflow from exploration to model deployment, engineering temporal and behavioral features and benchmarking an ANN against XGBoost and Logistic Regression.</p><ul><li>Python</li><li>ANN</li><li>XGBoost</li><li>Logistic Regression</li></ul><span class="project-link">View case study ↗</span></div>
      </a>
      <a class="project-card project-wide reveal" data-category="analytics" href="{{ '/projects/students-acohol-consumption' | relative_url }}">
        <div class="project-image project-image-photo"><img src="{{ '/assets/pngs/gummy.jpg' | relative_url }}" alt="Colorful gummy bears used as the project cover" loading="lazy"><span>Analytics</span></div>
        <div class="project-body"><p class="project-index">02 · Interactive analytics</p><h3>Students’ alcohol consumption</h3><p>Explored how family background, academic performance, and health factors relate to weekend alcohol consumption using interactive Altair dashboards.</p><ul><li>Python</li><li>Altair</li><li>Vega-Lite</li><li>EDA</li></ul><span class="project-link">View project ↗</span></div>
      </a>
      <a class="project-card project-wide reveal" data-category="ml analytics" href="{{ '/projects/amazon' | relative_url }}">
        <div class="project-image project-image-photo"><img src="{{ '/assets/pngs/fixing.jpg' | relative_url }}" alt="ReviewLens Amazon product analytics project cover" loading="lazy"><span>Full-stack analytics</span></div>
        <div class="project-body"><p class="project-index">03 · Data product</p><h3>ReviewLens: Amazon product discovery</h3><p>Led a full-stack discovery platform spanning 13.18M cleaned reviews and 2.04M products, combining Python ETL, React dashboards, and PostgreSQL ranking for reviewer analysis, hidden-gem discovery, and co-purchase recommendations.</p><ul><li>React</li><li>PostgreSQL</li><li>Express</li><li>SQL Optimization</li></ul><span class="project-link">View project ↗</span></div>
      </a>
      <a class="project-card project-wide reveal" data-category="ml research" href="https://doi.org/10.3390/s24154955">
        <div class="project-image project-image-taipei"><div class="map-grid"></div><span>2024</span><small>peer-reviewed publication</small></div>
        <div class="project-body"><p class="project-index">04 · Publication</p><h3>Tai Chi expertise classification</h3><p>Co-authored research on the classification of Tai Chi expertise, published in Sensors, volume 24, issue 15.</p><ul><li>Classification</li><li>Biomechanics</li><li>Health analytics</li></ul><span class="project-link">Read publication ↗</span></div>
      </a>
      <a class="project-card project-wide reveal" data-category="ml research" href="{{ '/projects/shopping-app-review-classification' | relative_url }}">
        <div class="project-image project-image-photo"><img src="{{ '/assets/pngs/shopping-app-classification/cover.svg' | relative_url }}" alt="Shopping app review classification pipeline" loading="lazy"><span>NLP · 11 classes</span></div>
        <div class="project-body"><p class="project-index">05 · Natural language processing</p><h3>Shopping app classification from reviews</h3><p>Built and evaluated text-classification baselines and a seven-model Transformer benchmark over 630K reviews, with DeBERTa-v3 reaching 0.7725 test Macro-F1.</p><ul><li>PyTorch</li><li>Transformers</li><li>DeBERTa</li><li>Macro-F1</li></ul><span class="project-link">View project ↗</span></div>
      </a>
    </div>
    <a class="all-work reveal" href="{{ '/projects/' | relative_url }}">See the full project archive <span>↗</span></a>
  </section>

  <section class="experience section" id="experience" aria-labelledby="experience-title">
    <div class="section-heading reveal"><div><p class="eyebrow">02 / Experience</p><h2 id="experience-title">Where I’ve learned &amp; built.</h2></div></div>
    <div class="timeline">
      <article class="timeline-row reveal"><p>2024—2026</p><div><h3>University of Pennsylvania</h3><span>MSE, Data Science · GPA 3.80/4.00</span></div><p>Graduate study in modern machine learning, scalable systems, and applied statistics.</p></article>
      <article class="timeline-row reveal"><p>Apr 2023—Aug 2024</p><div><h3>Mobility &amp; Fall Prevention Research Laboratory</h3><span>Data Science Researcher · Champaign, IL</span></div><p>Built a reproducible Python/MNE EEG connectivity pipeline and wearable-signal feature framework, improving research turnaround by 5× and reaching ~90% classification accuracy.</p></article>
      <article class="timeline-row reveal"><p>Jun—Jul 2023</p><div><h3>Feisuan Software Technology</h3><span>Data Scientist Intern · Shenzhen, CN</span></div><p>Built gradient-boosted models for personal-loan risk and tracked precision, recall, AUC (0.84), Gini coefficient, and false approval rate against underwriting thresholds.</p></article>
      <article class="timeline-row reveal"><p>Sep 2022—Feb 2023</p><div><h3>Center for Health Informatics Mobilizing Experts in Illinois</h3><span>Data Science Researcher · Champaign, IL</span></div><p>Used analytical SQL and Census-linked ICD-10 data to study mortality disparities across 10+ years and 15 geographic segments.</p></article>
      <article class="timeline-row reveal"><p>2020—2024</p><div><h3>University of Illinois Urbana-Champaign</h3><span>BS, Information Sciences + Data Science · GPA 3.90/4.00</span></div><p>Dean’s List; course assistant for Data Science Exploration and vice president of the Data Science Club.</p></article>
    </div>
  </section>

  <section class="about section" id="about" aria-labelledby="about-title">
    <div class="about-main reveal"><p class="eyebrow">03 / About</p><h2 id="about-title">I like figuring out why things happen—<br>and what to do next.</h2><p>I work across the full data-science lifecycle: wrangling complex data, engineering meaningful features, building and evaluating models, and translating results into decisions. My experience spans physiological signals, health outcomes, financial risk, and customer behavior.</p></div>
    <div class="toolkit reveal"><p class="eyebrow">Toolkit</p><div class="skill-list"><span>Python</span><span>Pandas</span><span>scikit-learn</span><span>PyTorch</span><span>SQL</span><span>R</span><span>XGBoost</span><span>LightGBM</span><span>Random Forest</span><span>SVM</span><span>Clustering</span><span>PCA</span><span>t-SNE</span><span>Time Series</span><span>A/B Testing</span><span>Causal Inference</span><span>Data Wrangling</span><span>Database Management</span><span>Visualization</span></div></div>
  </section>

  <section class="journal-preview section" aria-labelledby="journal-title">
    <div class="section-heading reveal">
      <div><p class="eyebrow">04 / Off the clock</p><h2 id="journal-title">Notes on things I like.</h2></div>
      <p>Not everything has to be a model. Sometimes it’s music, games, and the personality hiding between the playlists.</p>
    </div>
    <div class="journal-grid">
      {% for post in site.posts limit:2 %}
      <a class="journal-card reveal" href="{{ post.url | relative_url }}">
        <p class="eyebrow">{{ post.tags | slice: 0, 2 | join: ' · ' }}</p>
        <h3>{{ post.title }}</h3>
        <p>{{ post.description }}</p>
        <span>{{ post.date | date: '%b %Y' }} · Read note ↗</span>
      </a>
      {% endfor %}
    </div>
    <a class="all-work reveal" href="{{ '/blog/' | relative_url }}">Visit the full blog <span>↗</span></a>
  </section>

  <section class="contact section reveal">
    <p class="eyebrow">Currently looking for what’s next</p>
    <h2>Open to internship &amp;<br>full-time opportunities.</h2>
    <a href="mailto:{{ site.author.email }}">{{ site.author.email }} <span>↗</span></a>
  </section>
</main>

<footer class="portfolio-footer">
  <p>© <span data-year></span> Mengyue Huang</p>
  <div><a href="https://www.linkedin.com/in/{{ site.author.linkedin }}">LinkedIn ↗</a><a href="https://github.com/{{ site.author.github }}">GitHub ↗</a></div>
  <button type="button" data-to-top>Back to top ↑</button>
</footer>
