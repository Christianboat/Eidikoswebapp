from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp, URL
from wtforms import ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PageForm(FlaskForm):
    hero_title = StringField('Hero Title', validators=[Optional(), Length(max=255)])
    hero_subtitle = StringField('Hero Subtitle', validators=[Optional(), Length(max=255)])
    hero_description = TextAreaField('Hero Description', validators=[Optional()])
    meta_description = TextAreaField('Meta Description', validators=[Optional()])
    is_coming_soon = BooleanField('Coming Soon Mode')
    submit = SubmitField('Save Page')

class SectionForm(FlaskForm):
    section_key = StringField('Section Key (e.g. intro, vision)', validators=[DataRequired(), Length(max=64)])
    title = StringField('Title', validators=[Optional(), Length(max=255)])
    content = TextAreaField('Content (HTML Supported)', validators=[Optional()])
    image_file = FileField('Section Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    video_url = StringField('Video URL (YouTube)', validators=[Optional(), Length(max=255)])
    order = StringField('Order', validators=[Optional()]) # Using StringField for simple integer input or IntegerField
    submit = SubmitField('Save Section')

class ItemForm(FlaskForm):
    title = StringField('Title')
    subtitle = StringField('Subtitle')
    content = TextAreaField('Content')
    image_file = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    icon = StringField('Icon Class (e.g. fas fa-star)', validators=[Length(max=50)])
    link_url = StringField('Link URL')
    link_text = StringField('Link Text')
    order = IntegerField('Order', default=0)
    submit = SubmitField('Save Item')

class ImpactMetricForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    icon = StringField('Icon Class (e.g. fas fa-chart-bar)')
    order = IntegerField('Order', default=0)
    submit = SubmitField('Save Metric')

class ProgramForm(FlaskForm):
    name = StringField('Program Name', validators=[DataRequired(), Length(max=255)])
    slug = StringField('Slug', validators=[DataRequired(), Regexp(r'^[a-z0-9\-]+$', message="Slug must be lowercase alphanumeric and hyphens."), Length(min=3, max=64)])
    type = SelectField('Type', choices=[
        ('competitions', 'Competitions'),
        ('training', 'Training'),
        ('recognition', 'Recognition'),
        ('awards', 'Awards'),
        ('trade_fairs', 'Trade Fairs'),
        ('custom', 'Custom')
    ], validators=[DataRequired()])
    excerpt = StringField('Excerpt', validators=[Optional(), Length(max=250)], description="Short summary for cards (70-140 chars recommended)")
    description = TextAreaField('Description', validators=[Optional()])
    category = SelectField('Category (Legacy)', choices=[
        ('youth_competitions', 'Youth Competitions'),
        ('professional_dev', 'Professional Development'),
        ('awards', 'Awards'),
        ('trade_fairs', 'Trade Fairs'),
        ('services', '360 Services'),
        ('custom_design', 'Custom Design')
    ])
    icon = StringField('Icon Class (e.g. fas fa-star)', validators=[Optional(), Length(max=64)])
    image = FileField('Program Image/Logo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    cta_url = StringField('CTA URL', validators=[Optional(), Length(max=255)], description="External link or internal path (e.g., /contact)")
    cta_text = StringField('CTA Button Text', validators=[Optional(), Length(max=50)], default="Learn More")
    is_featured = BooleanField('Show on Homepage Highlight Section')
    order = IntegerField('Display Order', validators=[Optional()], default=0)
    submit = SubmitField('Save Program')

    def __init__(self, *args, **kwargs):
        self.original_slug = kwargs.pop('original_slug', None)
        super(ProgramForm, self).__init__(*args, **kwargs)

    def validate_slug(self, slug):
        from app.models import Program
        if self.original_slug and slug.data == self.original_slug:
            return
        prog = Program.query.filter_by(slug=slug.data).first()
        if prog:
            raise ValidationError('This slug is already in use. Please choose another.')

class ProgramSubContentForm(FlaskForm):
    title = StringField('Title/Header', validators=[Optional(), Length(max=255)])
    content = TextAreaField('Content (Use new lines for list items)', validators=[DataRequired()])
    order = IntegerField('Display Order', validators=[Optional()], default=0)
    submit = SubmitField('Save Content')

class TeamMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    title = StringField('Title', validators=[Optional(), Length(max=128)])
    bio = TextAreaField('Bio', validators=[Optional()])
    photo_url = StringField('Photo URL (Legacy)', validators=[Optional(), Length(max=255)])
    image_file = FileField('Upload Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Save Member')

class PartnershipForm(FlaskForm):
    type = SelectField('Type', choices=[
        ('schools', 'Schools'),
        ('corporate', 'Corporate'),
        ('embassies', 'Embassies'),
        ('universities', 'Universities'),
        ('publishers', 'Publishers'),
        ('custom', 'Custom')
    ])
    title = StringField('Title', validators=[Optional(), Length(max=255)])
    description = TextAreaField('Description', validators=[Optional()])
    benefits = TextAreaField('Benefits (One per line)', validators=[Optional()])
    logo_url = StringField('Logo URL (Legacy)', validators=[Optional(), Length(max=255)])
    image_file = FileField('Upload Logo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Save Partnership')

class NewsArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    category = StringField('Category (e.g. Awards, Digital)', validators=[Optional(), Length(max=64)])
    date_published = DateField('Date Published', format='%Y-%m-%d', validators=[Optional()])
    content = TextAreaField('Content', validators=[Optional()])
    excerpt = TextAreaField('Excerpt', validators=[Optional()])
    featured_image_url = StringField('Image URL (Legacy)', validators=[Optional(), Length(max=255)])
    image_file = FileField('Upload Featured Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Save Article')

class TestimonialForm(FlaskForm):
    author_name = StringField('Author Name', validators=[Optional(), Length(max=128)])
    author_role = StringField('Role / Title', validators=[Optional(), Length(max=128)])
    content = TextAreaField('Quote', validators=[DataRequired()])
    author_photo_url = StringField('Photo URL (Legacy)', validators=[Optional(), Length(max=255)])
    image_file = FileField('Upload Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Save Testimonial')



class ContactInfoForm(FlaskForm):
    email = StringField('Email', validators=[Optional(), Length(max=128)])
    phone = StringField('Phone', validators=[Optional(), Length(max=64)])
    address = TextAreaField('Address', validators=[Optional()])
    hours = TextAreaField('Office Hours', validators=[Optional()])
    submit = SubmitField('Save Contact Info')

class SocialMediaForm(FlaskForm):
    platform = SelectField('Platform', choices=[
        ('LinkedIn', 'LinkedIn'),
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
        ('YouTube', 'YouTube'),
        ('Twitter', 'Twitter'),
        ('X', 'X')
    ])
    url = StringField('URL', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Save Social Link')

class SiteSettingsForm(FlaskForm):
    site_name = StringField('Site Name / Brand', validators=[Optional(), Length(max=128)])
    footer_description = TextAreaField('Footer Description', validators=[Optional()])
    copyright_text = StringField('Copyright Text', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Save Site Settings')

class SponsorForm(FlaskForm):
    name = StringField('Sponsor Name', validators=[DataRequired(), Length(max=128)])
    logo_file = FileField('Sponsor Logo', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'])])
    order = IntegerField('Order', default=0)
    submit = SubmitField('Save Sponsor')

class SponsorshipTierForm(FlaskForm):
    tier_name = StringField('Tier Name (e.g. Platinum Partner)', validators=[DataRequired(), Length(max=128)])
    benefits = TextAreaField('Benefits (One per line)', validators=[Optional()])
    order = IntegerField('Display Order', default=0)
    submit = SubmitField('Save Tier')

class GalleryItemForm(FlaskForm):
    title = StringField('Caption / Title', validators=[Optional(), Length(max=255)])
    category = StringField('Category (e.g. Event, Competition)', validators=[Optional(), Length(max=64)])
    image_file = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    video_url = StringField('Video URL (YouTube/Drive)', validators=[Optional(), Length(max=255)])
    program_id = SelectField('Link to Program', coerce=int, validators=[Optional()])
    order = IntegerField('Display Order', default=0)
    submit = SubmitField('Save Gallery Item')

    def __init__(self, *args, **kwargs):
        super(GalleryItemForm, self).__init__(*args, **kwargs)
        from app.models import Program
        self.program_id.choices = [(0, '--- No Program ---')] + [(p.id, p.name) for p in Program.query.order_by(Program.name).all()]

