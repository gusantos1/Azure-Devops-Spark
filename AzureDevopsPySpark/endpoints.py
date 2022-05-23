class Endpoint:
    @classmethod
    def team_iterations(cls, organization: str, project: str, squad: str) -> str:
        """
            Get a team's iterations.
            https://docs.microsoft.com/en-us/rest/api/azure/devops/work/iterations/list?view=azure-devops-rest-6.0
        """
        return f'https://dev.azure.com/{organization}/{project}/{squad}/_apis/work/teamsettings/iterations?api-version=6.0'

    @classmethod    
    def team_backlog(cls, organization: str, project: str, squad: str) -> str:
        """
            List all backlog levels.
            https://docs.microsoft.com/en-us/rest/api/azure/devops/work/backlogs/list?view=azure-devops-rest-6.0
        """
        return f'https://dev.azure.com/{organization}/{project}/{squad}/_apis/work/backlogs?api-version=6.0-preview.1'
    
    @classmethod    
    def backlog_items(cls, organization: str, project: str, squad: str, level: str) -> str:
        """
            Get a list of work items within a backlog level.
            https://docs.microsoft.com/en-us/rest/api/azure/devops/work/backlogs/get-backlog-level-work-items?view=azure-devops-rest-6.0
        """
        return f'https://dev.azure.com/{organization}/{project}/{squad}/_apis/work/backlogs/{level}/workItems?api-version=6.0-preview.1'
    
    @classmethod
    def work_item_in_iteration(cls, organization: str, project: str, squad: str, iteration_id: str) -> str:
        """
            Get the `IDs` of all work items within the iteration(sprint) of a squad.
            https://docs.microsoft.com/en-us/rest/api/azure/devops/work/iterations/get-iteration-work-items?view=azure-devops-rest-6.0
            
        """
        return f'https://dev.azure.com/{organization}/{project}/{squad}/_apis/work/teamsettings/iterations/{iteration_id}/workitems?api-version=6.0-preview.1'
    
    @classmethod
    def all_teams(cls, organization: str, params: str = None) -> str:
        """
            Get a list of all teams.
            https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-all-teams?view=azure-devops-rest-6.0
        """
        if params:
            return f"https://dev.azure.com/{organization}/_apis/teams?{params}&api-version=6.0-preview.3"
        return f"https://dev.azure.com/{organization}/_apis/teams?api-version=6.0-preview.3"
    
    @classmethod
    def all_members(cls, organization: str, project: str, squad: str, params: str = None) -> str:
        """
            Get a list of members for a specific team.
            https://docs.microsoft.com/en-us/rest/api/azure/devops/core/teams/get-team-members-with-extended-properties?view=azure-devops-rest-6.0       
        """
        if params:
            return f"https://dev.azure.com/{organization}/_apis/projects/{project}/teams/{squad}/members?{params}&api-version=6.1-preview.2"
        return f"https://dev.azure.com/{organization}/_apis/projects/{project}/teams/{squad}/members?api-version=6.1-preview.2"
    
    @classmethod
    def work_items(cls, organization: str, project: str, id: str, fields: str) -> str:
        """
            Returns a work item by its id. `Can receive a string with a maximum of 200 ids`.
            https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/get-work-item?view=azure-devops-rest-6.0
        """
                        
        return f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems?ids={id}&fields={fields}&api-version=6.0"
 
    @classmethod
    def wiql(cls, organization: str, project: str, params: str = None) -> str:
        """
            Returns all work items for a project.
            https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/wiql/query-by-wiql?view=azure-devops-rest-6.0
        """
        if params:
            return f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?{params}&api-version=6.0"
        return f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0"
    
    @classmethod
    def tags(cls, organization: str, project: str) -> str:
        """
            Returns all tags for a project.
        """
        return f'https://dev.azure.com/{organization}/{project}/_apis/wit/tags?api-version=6.0-preview.1'
    
    @classmethod
    def build(cls, organization: str, project: str) -> str:
        """
            Just to return 200 quickly.
            https://docs.microsoft.com/en-us/rest/api/azure/devops/build/builds/list?view=azure-devops-rest-6.0
        """
        return f"https://dev.azure.com/{organization}/{project}/_apis/build/builds?api-version=6.0"
  
    @classmethod
    def all_process(cls, organization: str):
        """
            Returns all processes in an organization.
        """
        return f'https://dev.azure.com/{organization}/_apis/work/processes?api-version=4.1-preview.1'
    
    @classmethod
    def list_work_item_types(cls, organization: str, process_id: str):
        """
            Returns all work item types associated with a process.
        """
        return f'https://dev.azure.com/{organization}/_apis/work/processdefinitions/{process_id}/workItemTypes/'
    
    @classmethod
    def project_reference(cls, organization: str, process_id: str):
        """
            Returns all projects associated with a process.
        """
        return f'https://dev.azure.com/{organization}/_apis/work/processes/{process_id}?$expand=projects&api-version=6.0-preview.2'
    
    @classmethod
    def fields_process(cls, organization: str, process_id: str, type_id: str):
        """
            Returns all fields associated with a process.
        """
        return f'https://dev.azure.com/{organization}/_apis/work/processdefinitions/{process_id}/workItemTypes/{type_id}/fields'