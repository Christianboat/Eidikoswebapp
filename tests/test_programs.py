import unittest
import os
import sys

# Add the app directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Program, FlagshipProgram, SiteSettings, SocialMedia, ContactInfo, Sponsor
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    DEBUG = False
    SERVER_NAME = 'localhost'

class ProgramTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Seed minimal data for base.html context processor
        db.session.add(SiteSettings(site_name="Eidikos Test"))
        db.session.add(ContactInfo(email="test@example.com"))
        db.session.commit()
        
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_program_slug_and_detail_url(self):
        """Test that Program model has slug and detail_url property works."""
        p = Program(name="Global Spell Bee", slug="global-spell-bee", type="competitions")
        db.session.add(p)
        db.session.commit()
        
        with self.app.test_request_context():
            self.assertEqual(p.slug, "global-spell-bee")
            self.assertEqual(p.detail_url, "/program/global-spell-bee")

    def test_flagship_slug_and_detail_url(self):
        """Test that FlagshipProgram model has slug and detail_url property works."""
        p = FlagshipProgram(name="Global Spell Bee", slug="global-spell-bee", type="competitions")
        db.session.add(p)
        db.session.commit()
        
        with self.app.test_request_context():
            self.assertEqual(p.slug, "global-spell-bee")
            self.assertEqual(p.detail_url, "/programs/global-spell-bee")

    def test_programs_listing_route(self):
        """Test that the general programs listing page renders correctly."""
        p1 = Program(name="Program 1", slug="p1", type="competitions", category="youth_competitions")
        p2 = FlagshipProgram(name="Flagship 1", slug="f1", type="training", category="professional_dev")
        db.session.add_all([p1, p2])
        db.session.commit()
        
        response = self.client.get('/programs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Program 1', response.data)
        self.assertIn(b'Flagship 1', response.data)

    def test_flagship_slug_uniqueness(self):
        """Test that slugs are unique for FlagshipPrograms."""
        p1 = FlagshipProgram(name="Unique 1", slug="unique", type="competitions")
        db.session.add(p1)
        db.session.commit()
        
        p2 = FlagshipProgram(name="Unique 2", slug="unique", type="training")
        db.session.add(p2)
        
        # This should raise integrity error due to unique constraint
        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_program_detail_route(self):
        """Test that program detail page renders correctly."""
        p = FlagshipProgram(
            name="Global Spell Bee", 
            slug="global-spell-bee", 
            type="competitions", 
            excerpt="World literacy competition",
            description="Detailed description here."
        )
        db.session.add(p)
        db.session.commit()
        
        response = self.client.get('/programs/global-spell-bee')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Global Spell Bee', response.data)
        self.assertIn(b'World literacy competition', response.data)
        self.assertIn(b'Detailed description here', response.data)

    def test_related_programs_logic(self):
        """Test that related programs of the same type are shown."""
        p1 = FlagshipProgram(name="Comp 1", slug="c1", type="competitions")
        p2 = FlagshipProgram(name="Comp 2", slug="c2", type="competitions")
        p3 = FlagshipProgram(name="Train 1", slug="t1", type="training")
        
        db.session.add_all([p1, p2, p3])
        db.session.commit()
        
        response = self.client.get('/programs/c1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comp 2', response.data)
        self.assertNotIn(b'Train 1', response.data)

    def test_program_404(self):
        """Test that non-existent slugs return 404."""
        response = self.client.get('/programs/non-existent-slug')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main(verbosity=2)
