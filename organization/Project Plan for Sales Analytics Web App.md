
## Project Overview
**Objective**: Develop a web application with a database to analyze a provided dataset, focusing on sales performance, product revenue comparisons, lifespan correlations, category metrics, and ingredient/category trends over time.  
**Presentation Date**: May 6, 2025  
**Completion Deadline**: July 1, 2025  
**Duration**: ~8 weeks (May 6, 2025 – July 1, 2025)  
**Goal**: Monitor product success post-launch and track lifecycle trends through a user-friendly web interface.  
**Note**: This is a university project, so deployment and User Acceptance Testing (UAT) are excluded, and JUnit tests are not required.

## Milestones and Work Packages

### Milestone 1: Project Kickoff and Planning
**Timeline**: May 6, 2025 – May 12, 2025  
**Objective**: Finalize project scope, architecture, and initial plans.  
**Work Packages**:  
- **WP1.1: Requirements Gathering** (May 6 – May 8)  
  - Analyze dataset structure and define key metrics (sales performance, revenue, lifespan, etc.).  
  - Identify user stories (e.g., “View sales performance curve since launch”).  
  - Define functional (e.g., data visualization, filtering) and non-functional (e.g., performance, security) requirements.  
  - Identify what “distance” means in the context of the dataset (e.g., time since launch, geographic distribution, or metric-based distance).  
  - **Output**: Requirements document.  
- **WP1.2: Architecture Planning** (May 8 – May 10)  
  - Design system architecture (e.g., client-server model, REST API, database schema).  
  - Choose tech stack (e.g., React for frontend, Node.js/Express for backend, PostgreSQL for database).  
  - Plan scalability and security considerations (e.g., authentication, data validation).  
  - **Output**: Architecture diagram and tech stack decision document.  
- **WP1.3: Project Timeline and Role Assignment** (May 10 – May 12)  
  - Break down tasks into sprints (e.g., 2-week sprints).  
  - Assign roles (e.g., frontend developer, backend developer, database engineer).  
  - Set up project management tools (e.g., Jira, Trello).  
  - **Output**: Gantt chart and sprint plan.

### Milestone 2: Backend Development and Database Setup
**Timeline**: May 13, 2025 – June 2, 2025  
**Objective**: Build and integrate the backend and database to handle data processing and API endpoints.  
**Work Packages**:  
- **WP2.1: Database Setup and Integration** (May 13 – May 20)  
  - Design database schema based on dataset (e.g., tables for products, sales, categories).  
  - Set up database (e.g., PostgreSQL) and import dataset.  
  - Implement indexing for performance (e.g., on product IDs, timestamps).  
  - Write scripts for data cleaning and preprocessing (e.g., handle missing values).  
  - **Output**: Populated database and preprocessing scripts.  
- **WP2.2: Backend Development** (May 20 – June 2)  
  - Develop REST API endpoints (e.g., `/sales/curve`, `/products/revenue/compare`).  
  - Implement business logic for analytics (e.g., calculate revenue trends, correlations).  
  - Add authentication (e.g., JWT) and input validation.  
  - Test API endpoints manually using tools like Postman.  
  - **Output**: Functional backend with documented API.

### Milestone 3: Frontend Development
**Timeline**: May 20, 2025 – June 16, 2025  
**Objective**: Create a responsive and interactive frontend for data visualization and user interaction.  
**Work Packages**:  
- **WP3.1: Frontend Wireframing and Design** (May 20 – May 27)  
  - Create wireframes for key pages (e.g., dashboard, product comparison).  
  - Design UI/UX with tools like Figma, focusing on usability (e.g., filters, charts).  
  - Plan visualizations (e.g., line charts for sales curves, bar charts for category metrics).  
  - **Output**: Wireframes and UI design mockups.  
- **WP3.2: Frontend Implementation** (May 27 – June 16)  
  - Set up React project with Tailwind CSS for styling.  
  - Implement components for visualizations (e.g., using Chart.js or D3.js).  
  - Connect frontend to backend APIs for dynamic data fetching.  
  - Add interactive features (e.g., date range filters, product category selectors).  
  - Ensure responsiveness across devices.  
  - **Output**: Functional frontend integrated with backend.

### Milestone 4: Testing and Finalization
**Timeline**: June 17, 2025 – July 1, 2025  
**Objective**: Ensure the application is functional, meets requirements, and is ready for presentation.  
**Work Packages**:  
- **WP4.1: Functional Testing** (June 17 – June 23)  
  - Perform manual testing of backend APIs and frontend components.  
  - Verify data accuracy (e.g., sales curves, revenue comparisons).  
  - Test edge cases (e.g., large datasets, invalid inputs).  
  - Fix identified bugs.  
  - **Output**: Bug-free application.  
- **WP4.2: Review and Final Improvements** (June 24 – July 1)  
  - Conduct internal review to ensure all requirements are met (e.g., visualizations, filters).  
  - Make minor UI/UX or performance improvements based on team feedback.  
  - Prepare presentation summarizing project outcomes.  
  - **Output**: Final application and presentation slides.

## Timeline Summary (Gantt Chart Style)
```
May 6        May 13       May 20       June 2       June 16      July 1
|----M1------|----M2------------------|----M3-------|-----M4------|
Planning     Database/Backend        Frontend     Testing/Finalization
             |-----------------Backend-----------------|
                          |------------Frontend------------|
```

## Notes
- **Overlap**: Frontend wireframing starts during backend development to align API requirements.  
- **Sprints**: Use 2-week sprints for iterative development and feedback.  
- **Risk Management**: Buffer time in June for unexpected delays (e.g., dataset issues).  
- **Team Collaboration**: Weekly standups to sync backend and frontend progress.  
- **Tools**: Git for version control, Slack for communication, Figma for design, Postman for API testing.  
- **Changes**: Removed deployment, UAT, and JUnit tests per university project constraints. Extended testing and finalization phase to cover manual testing and improvements.