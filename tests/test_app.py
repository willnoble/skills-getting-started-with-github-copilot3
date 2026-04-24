"""Integration tests for the Mergington High School FastAPI application.

Tests are structured using the AAA pattern:
- Arrange: Set up test fixtures and data
- Act: Perform the API operation
- Assert: Verify the result
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_all_activities_returns_success(self, client):
        """Arrange: client is ready
        Act: Make GET request to /activities
        Assert: Verify 200 status and dict response
        """
        # Arrange
        # (client fixture already provides TestClient instance)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_activities_includes_preloaded_activities(self, client):
        """Verify response includes all 9 pre-loaded activities."""
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Soccer Club",
            "Art Club",
            "Drama Club",
            "Debate Club",
            "Science Club"
        ]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_returns_complete_activity_structure(self, client, sample_activity_name):
        """Verify each activity has all required fields."""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()
        activity = activities[sample_activity_name]

        # Assert
        for field in required_fields:
            assert field in activity
        assert isinstance(activity["participants"], list)

    def test_get_activities_participants_list_contains_emails(self, client, sample_activity_name):
        """Verify participants list contains valid data."""
        # Arrange
        # (sample_activity_name="Chess Club" has pre-loaded participants)

        # Act
        response = client.get("/activities")
        activities = response.json()
        participants = activities[sample_activity_name]["participants"]

        # Assert
        assert len(participants) > 0
        assert all("@" in email for email in participants)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful_adds_participant(self, client, sample_activity_name, sample_email):
        """Arrange: Prepare activity and new email
        Act: POST signup request
        Assert: Verify email added to participants
        """
        # Arrange
        response_before = client.get("/activities")
        participants_before = response_before.json()[sample_activity_name]["participants"]

        # Act
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        assert "signed up" in response.json()["message"].lower()
        
        # Verify participant was actually added
        response_after = client.get("/activities")
        participants_after = response_after.json()[sample_activity_name]["participants"]
        assert sample_email in participants_after
        assert len(participants_after) == len(participants_before) + 1

    def test_signup_returns_confirmation_message(self, client, sample_activity_name, sample_email):
        """Verify response includes expected confirmation message."""
        # Arrange
        # (fixtures provide activity and email)

        # Act
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert sample_email in response_data["message"]
        assert sample_activity_name in response_data["message"]

    def test_signup_to_nonexistent_activity_returns_404(self, client, nonexistent_activity_name, sample_email):
        """Arrange: Prepare nonexistent activity name
        Act: POST signup to invalid activity
        Assert: Verify 404 status
        """
        # Arrange
        # (nonexistent_activity_name fixture provides invalid name)

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_email_returns_400(self, client, sample_activity_name):
        """Arrange: Note existing participant in Chess Club
        Act: Try to sign up same email twice
        Assert: Verify 400 duplicate error
        """
        # Arrange
        # Chess Club has pre-loaded participant: michael@mergington.edu
        duplicate_email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": duplicate_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_multiple_different_students_to_same_activity(self, client, sample_activity_name):
        """Verify multiple different students can sign up for the same activity."""
        # Arrange
        email1 = "student.one@mergington.edu"
        email2 = "student.two@mergington.edu"

        # Act - First student
        response1 = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email1}
        )
        # Act - Second student
        response2 = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email2}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        response_final = client.get("/activities")
        participants = response_final.json()[sample_activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_participant_successful(self, client, sample_activity_name):
        """Arrange: Identify existing participant in Chess Club
        Act: DELETE request to remove participant
        Assert: Verify participant removed
        """
        # Arrange
        # Chess Club has pre-loaded participant: michael@mergington.edu
        email_to_remove = "michael@mergington.edu"
        response_before = client.get("/activities")
        participants_before = response_before.json()[sample_activity_name]["participants"]

        # Act
        response = client.delete(
            f"/activities/{sample_activity_name}/participants/{email_to_remove}"
        )

        # Assert
        assert response.status_code == 200
        assert "removed" in response.json()["message"].lower()
        
        # Verify participant was actually removed
        response_after = client.get("/activities")
        participants_after = response_after.json()[sample_activity_name]["participants"]
        assert email_to_remove not in participants_after
        assert len(participants_after) == len(participants_before) - 1

    def test_remove_participant_returns_confirmation_message(self, client, sample_activity_name):
        """Verify response includes expected removal confirmation."""
        # Arrange
        email_to_remove = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{sample_activity_name}/participants/{email_to_remove}"
        )

        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert email_to_remove in response_data["message"]
        assert sample_activity_name in response_data["message"]

    def test_remove_from_nonexistent_activity_returns_404(self, client, nonexistent_activity_name, sample_email):
        """Arrange: Prepare invalid activity name
        Act: DELETE from nonexistent activity
        Assert: Verify 404 status
        """
        # Arrange
        # (nonexistent_activity_name fixture provides invalid name)

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity_name}/participants/{sample_email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_remove_nonexistent_participant_returns_404(self, client, sample_activity_name, sample_email):
        """Arrange: Use email not in Chess Club participants
        Act: DELETE request for nonexistent participant
        Assert: Verify 404 status
        """
        # Arrange
        # sample_email (test.student@mergington.edu) is not pre-loaded in any activity

        # Act
        response = client.delete(
            f"/activities/{sample_activity_name}/participants/{sample_email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_remove_participant_then_readd_same_email(self, client, sample_activity_name):
        """Verify same email can be re-added after removal."""
        # Arrange
        email = "michael@mergington.edu"

        # Act - Remove
        response_remove = client.delete(
            f"/activities/{sample_activity_name}/participants/{email}"
        )

        # Act - Re-add
        response_readd = client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response_remove.status_code == 200
        assert response_readd.status_code == 200
        
        response_final = client.get("/activities")
        participants = response_final.json()[sample_activity_name]["participants"]
        assert email in participants
