from django.test import TestCase
from django.contrib.auth.models import User
from .models import TutorRequest, TutoringUser, TutorRequestAccount
import datetime

class TutorRequestTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1password')
        self.user2 = User.objects.create_user(username='user2', password='user2password')
        self.tutoring_user1 = TutoringUser.objects.create(user=self.user1, is_tutor=True, full_name='Tutor 1', major='ECE')
        self.tutoring_user2 = TutoringUser.objects.create(user=self.user2, is_tutor=True, full_name='Tutor 2', major='CS')

    def test_tutor_request_creation(self):
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)

        tutor_request = TutorRequest.objects.create(
            request_user=self.user1.username,
            request_tutor=self.user2.username,
            request_startTime=start_time,
            request_endTime=end_time
        )

        self.assertEqual(tutor_request.request_user, self.user1.username)
        self.assertEqual(tutor_request.request_tutor, self.user2.username)
        self.assertEqual(tutor_request.request_startTime, start_time)
        self.assertEqual(tutor_request.request_endTime, end_time)
        self.assertFalse(tutor_request.is_verified)

class TutoringUserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.tutoring_user = TutoringUser.objects.create(user=self.user, full_name='John Doe', major='ECE')

    def test_tutoring_user_creation(self):
        self.assertEqual(self.tutoring_user.user, self.user)
        self.assertEqual(self.tutoring_user.full_name, 'John Doe')
        self.assertEqual(self.tutoring_user.major, 'ECE')
        self.assertFalse(self.tutoring_user.is_tutor)

class TutorRequestAccountTestCase(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(username='student', password='studentpassword')
        self.tutor = User.objects.create_user(username='tutor', password='tutorpassword')
        self.tutoring_user = TutoringUser.objects.create(user=self.tutor, is_tutor=True, full_name='Tutor', major='ECE')

    def test_tutor_request_account_creation(self):
        session_date = datetime.date.today()
        session_time = datetime.time(hour=10, minute=0)
        pay_rate = 25.00

        tutor_request_account = TutorRequestAccount.objects.create(
            student=self.student,
            tutor=self.tutor,
            session_date=session_date,
            session_time=session_time,
            pay_rate=pay_rate,
            status='pending'
        )

        self.assertEqual(tutor_request_account.student, self.student)
        self.assertEqual(tutor_request_account.tutor, self.tutor)
        self.assertEqual(tutor_request_account.session_date, session_date)
        self.assertEqual(tutor_request_account.session_time, session_time)
        self.assertEqual(tutor_request_account.pay_rate, pay_rate)
        self.assertEqual(tutor_request_account.status, 'pending')
