@router.get("/kuriftu-services/", response_model=list[schemas.KuriftuService])
def get_kuriftu_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    services = db_service.get_kuriftu_services(db, skip=skip, limit=limit)
    return services