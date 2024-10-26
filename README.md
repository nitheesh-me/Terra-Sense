<p align="center">
  <a href="" rel="noopener">
 <img src="./docs/assets/images/megathon24.png" alt="Megathon 24"></a>
</p>
<h3 align="center">Predicting Natural disasters using satellite data</h3>

<div align="center">

<!-- https://dev.to/envoy_/150-badges-for-github-pnk -->
<!-- https://app.logomakr.com/ -->

[![Hackathon](https://img.shields.io/badge/hackathon-Megathon\%20'24-purple.svg)](https://megathon.in/) [![Status](https://img.shields.io/badge/status-draft-yellow.svg)]()
<!-- [![GitHub Issues](https://img.shields.io/github/issues/nitheesh-me/....svg)](https://github.com/nitheesh-me/.../issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/nitheesh-me/....svg)](https://github.com/nitheesh-me/.../pulls) -->
[![License](https://img.shields.io/badge/license-Creative%20Commons%20Zero%20v1.0%20Universal-blue.svg)](https://creativecommons.org/public-domain/cc0/)

<!-- [![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)](https://python.org/) [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/) [![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/) [![Bun](https://img.shields.io/badge/Bun-FF2D20?style=for-the-badge&logo=bun&logoColor=white)](https://bun.sh) -->
</div>

---

<p align="center"> identifies patterns or risk factors that
indicate the onset of these disasters
    <br>
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 Problem Statement ](#-problem-statement-)
  - [Specifications](#specifications)
- [💡 Idea / Solution ](#-idea--solution-)
- [⛓️ Dependencies / Limitations ](#️-dependencies--limitations-)
- [🚀 Future Scope ](#-future-scope-)
  - [Other considerations](#other-considerations)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [🎈 Usage ](#-usage-)
- [⛏️ Built With ](#️-built-with-)
- [✍️ Authors ](#️-authors-)
- [🎉 Acknowledgments ](#-acknowledgments-)

## 🧐 Problem Statement <a name = "problem_statement"></a>

Create a model that identifies patterns or risk factors that indicate the onset of these disasters. Use satellite imagery and relevant data to predict natural disasters (floods, landslides, etc.)

**Expected outcomes**:

1. *AI Prediction Model*:
 Build a model to predict natural disasters (floods, landslides) using satellite data.The model
should analyze environmental factors to estimate disaster likelihood.
2. *Data Monitoring*:
 Track real-time changes in weather patterns and soil conditions using satellite data.
Provide insights or visualizations of these environmental changes.
3. *Real-Time Alerts:*
 Develop a mobile/web application that delivers disaster alerts to at-risk communities in
real time.

**Key considerations**:

- Focus on Key Indicators: Monitor rainfall, soil moisture, and terrain changes.
- Accuracy Matters: Ensure predictions are based on clean, reliable satellite data.
- Real-Time Performance: The system should quickly analyze data and send alerts without delays.
- Scalability: Make sure the solution can be adapted for different regions and disasters.
- User-Friendly Alerts: Notifications should be easy to understand and act on.

### Specifications

- *IDEAL*: Develop a comprehensive system that includes a real-time predictive model for flood risk, a monitoring system for landslide indicators, and a mobile/web application for delivering clear disaster alerts to at-risk communities based on satellite data and environmental factors.

- *REALITY*: Current models rely on historical data, existing monitoring systems lack integration with satellite imagery, and alert mechanisms are often slow and impersonal, relying on traditional media.

*CONSEQUENCES*: Inaccurate predictions and delayed alerts can lead to loss of life, property damage, unanticipated disasters, and diminished trust in emergency services, ultimately undermining community safety and resilience.

## 💡 Idea / Solution <a name = "idea"></a>

> [!IMPORTANT] TL;DR
> Develop a real-time disaster prediction and alert system that leverages satellite imagery and data analytics to provide timely alerts and insights to at-risk communities. This uses machine learning to predict disasters and assess their impact, with a user-friendly interface for residents and authorities.

Check out the [SOLUTION.md](./SOLUTION.md) file for a detailed explanation of the solution.


## ⛓️ Dependencies / Limitations <a name = "limitations"></a>

**Dependencies**
- *Data Availability and Quality*:
  The project relies on high-quality satellite imagery and real-time environmental data. Inconsistent access can hinder model accuracy.
- *Technological Infrastructure*:
  Effective alert dissemination depends on robust internet connectivity and access to mobile devices. Poor connectivity limits reach.
- *Collaboration with Local Authorities*:
  Success requires cooperation from disaster management agencies for data sharing and resource support. Lack of collaboration can create gaps.

**Limitations**
- *Data Accessibility*:
  Limited access to real-time environmental data due to regulatory restrictions may reduce predictive accuracy. This could delay disaster responses. Future research could explore open data initiatives.
- *Technological Reliance*:
  Assumes all community members have access to smartphones or the internet. The digital divide may leave some populations at risk. Further research on alternative communication methods is needed.
- *Behavioral Response Variability*:
  Individuals may not respond to alerts as expected due to past experiences or misinformation. This could diminish system effectiveness, indicating a need for effective communication strategies.
- *Model Generalization*:
  The predictive model may not apply universally across regions with different environmental conditions and community characteristics, leading to inaccuracies. Future research should focus on adapting the model to diverse contexts.

## 🚀 Future Scope <a name = "future_scope"></a>

During the Hackathon, several key components were not fully developed:

- *Advanced Predictive Analytics*: Further refinement of the predictive model is needed to enhance accuracy by incorporating more variables like socioeconomic factors.

- *User Engagement Features*: Initial alerts lack gamification and community involvement elements to encourage active participation in data reporting and preparedness.

- *Integration with Local Resources*: A comprehensive directory of emergency services and shelters was not included, limiting access to critical information.

- *Multi-Language Support*: The application currently operates in one language, restricting accessibility for diverse communities.

**Future Achievements**

In the future, the project can achieve:

- *Enhanced Predictive Accuracy*: Incorporating machine learning and diverse datasets will improve the model's reliability.

- *Real-Time Community Feedback Loop*: Enabling users to report local conditions will enhance data accuracy and engagement.

- *Comprehensive Disaster Management Toolkit*: Tools for local authorities can improve damage assessment and resource allocation.

- *Broader Community Outreach*: Expanding partnerships will increase awareness and adoption, benefiting more communities.

- *Scalable Model*: Future iterations can adapt the system for different regions and disaster types, enhancing global resilience.

Addressing these areas will improve disaster preparedness and response, ultimately saving lives and reducing property loss.

### Other considerations

- AR/VR for disaster prediction and training
- Collaborative Community Mapping
- Dynamic Scenario Planning
- Integration with Smart Home Technology

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites

- [Bun](https://bun.sh) (v1.1.32)

### Installing

To install dependencies:

```bash
bun install
```

To run:

```bash
bun run index.ts
```

## 🎈 Usage <a name="usage"></a>

Add notes about how to use the system.

## ⛏️ Built With <a name = "tech_stack"></a>

- [MongoDB](https://www.mongodb.com/) - Database
- [Express](https://expressjs.com/) - Server Framework
- [VueJs](https://vuejs.org/) - Web Framework
- [NodeJs](https://nodejs.org/en/) - Server Environment

## ✍️ Authors <a name = "authors"></a>

- [@kylelobo](https://github.com/kylelobo) - Idea & Initial work

See also the list of [contributors](https://github.com/kylelobo/The-Documentation-Compendium/contributors)
who participated in this project.

## 🎉 Acknowledgments <a name = "acknowledgments"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References
