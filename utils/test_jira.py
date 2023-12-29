from atlassian import Jira
import simplejson as json

jira = Jira(url="https://jira.kyoffice.cn", username="yaoshaoqiang@newcowin.com", password="ysq198923_")

# data = jira.project(key="TSP")
# data = jira.get_issue(issue_id_or_key="TSP-105")
# data = jira.get_project_versions(key="TSP")
# data = jira.get_all_project_issues(project="TSP")
data = jira.get_all_statuses()
# jql = "project=TSP AND fixVersion=11416"
# data = jira.jql(jql)
print(data)

# data = jira.update_version(
#                 project_key="TSP",
#                 project_id="10400",
#                 version="test11"
#             )
print(json.dumps(data, indent=4))
