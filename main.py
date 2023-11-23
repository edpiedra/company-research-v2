
if __name__=="__main__":
    from modules.company_research import * 
    
    company_research = CompanyResearch()
    company_research.app.run_server(port=8050)