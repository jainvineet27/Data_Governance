# Data_Governance
echo "# Data_Governance" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/jainvineet27/Data_Governance.git
git push -u origin main

Databricks Connect VSCode se Volumes access nahi kar sakta.
Volumes = Unity Catalog storage  
Databricks Connect = local Spark session

Local Spark session UC Volumes ko mount nahi kar sakta, isliye tumko error mil raha hai.
⭐ Why Databricks Connect cannot access Volumes
Because:

Volumes = Unity Catalog + cloud storage

Databricks Connect = local Spark

Local Spark has no UC authentication

Local Spark has no access to cloud storage

Local Spark cannot mount /Volumes or /mnt

👉 Only Databricks cluster can access UC Volumes.
⭐ Final Answer
Your SQL is correct.
The error is because Databricks Connect cannot access UC Volumes.
Run this SQL inside Databricks, not VSCode.
