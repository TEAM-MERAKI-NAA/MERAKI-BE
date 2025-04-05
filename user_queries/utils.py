from .models import CommunityRequest, Community

def approve_request(request_id):
    """
    Approve a community creation request and create the community.
    """
    # Retrieve the community request with status 'pending'
    community_request = CommunityRequest.objects.get(id=request_id, status='pending')
    # Update the request status to 'approved'
    community_request.status = 'approved'
    community_request.save()

    # Create a new community based on the request
    Community.objects.create(
        name=community_request.name,
        description=community_request.description,
        category=community_request.proposed_category
    )
