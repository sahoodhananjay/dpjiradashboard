Product or service quality often serves as a key differentiating factor for companies. At Dialpad, we rely on tools like Jira and Domo to collect and analyze customer feedback. While these platforms provide valuable insights into overall product performance, they fall short when it comes to delivering detailed, granular-level reports on product health.

To address this gap, we've developed a dynamic Dialpad Product Health Monitoring Dashboard. This dashboard analyzes customer-reported defects and defines product health using four distinct quality metrics, visualized through interactive graphs. The application is hosted on the Heroku platform, integrated with Google OAuth for secure access, and is available exclusively to Dialpad users.

Dashboard Features
Product health is assessed through four automatically updating graphs, refreshed every 30 minutes. These graphs display data across four time periods: Last 11 Months, Last 9 Months, Last 3 Months, and the Current Month.

The four key quality metrics include:

Customer Reported Defects
Tracks the average number of customer-reported product defects for three core Seal Teams: Talk, Contact Center, and Integration.

Defect Priority
Shows the distribution of reported defects by priority level: Urgent, High, Medium, and Low.

Resolution Status
Categorizes reported defects by resolution outcome: Fixed, Backlog, or Noise (non-actionable issues).

Mean Time to Resolve (MTTR)
Measures the average number of days taken by the development team to resolve customer-reported issues.

usage: https://dpjiradashboard.herokuapp.com/

