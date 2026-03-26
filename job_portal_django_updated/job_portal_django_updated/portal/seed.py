"""
Run with:  python manage.py shell < portal/seed.py
           OR:  python manage.py loaddata (after converting to fixtures)

Creates demo users and sample jobs.
"""
from portal.models import User, Job

# Demo users
if not User.objects.filter(email='user@example.com').exists():
    u = User(
        username='user@example.com',
        email='user@example.com',
        first_name='John',
        last_name='Doe',
        role='user',
        avatar='https://cdn-icons-png.flaticon.com/512/3789/3789820.png'
    )
    u.set_password('password')
    u.save()
    print('Created user: user@example.com / password')

if not User.objects.filter(email='admin@example.com').exists():
    a = User(
        username='admin@example.com',
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        role='admin',
        is_staff=True,
        avatar='https://cdn-icons-png.flaticon.com/512/9079/9079615.png'
    )
    a.set_password('admin')
    a.save()
    print('Created admin: admin@example.com / admin')

# Sample jobs
sample_jobs = [
    {
        'title': 'Senior Frontend Developer', 'company': 'TechCorp Inc.',
        'location': 'San Francisco, CA', 'type': 'Full-time',
        'salary': '$120,000 – $160,000',
        'description': 'We are looking for an experienced Frontend Developer to join our growing team. You will be responsible for building high-quality web applications using modern frameworks.',
        'requirements': '5+ years of experience with React and TypeScript\nStrong understanding of web performance optimization\nExperience with state management libraries\nExcellent problem-solving skills\nStrong communication and teamwork abilities',
        'logo': 'https://images.unsplash.com/photo-1549924231-f129b911e442?w=100&h=100&fit=crop',
    },
    {
        'title': 'Product Designer', 'company': 'DesignHub',
        'location': 'Remote', 'type': 'Full-time',
        'salary': '$90,000 – $130,000',
        'description': 'Join our design team to create beautiful and intuitive user experiences. You will work closely with product managers and engineers to bring ideas to life.',
        'requirements': '3+ years of product design experience\nProficiency in Figma and Adobe Creative Suite\nStrong portfolio demonstrating UX/UI skills\nExperience with design systems\nAbility to work in a fast-paced environment',
        'logo': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=100&h=100&fit=crop',
    },
    {
        'title': 'Backend Engineer', 'company': 'DataFlow Systems',
        'location': 'New York, NY', 'type': 'Full-time',
        'salary': '$130,000 – $170,000',
        'description': 'We need a talented Backend Engineer to help build scalable APIs and services. You will work on challenging problems involving large-scale data processing.',
        'requirements': '4+ years of backend development experience\nProficiency in Node.js, Python, or Go\nExperience with databases (SQL and NoSQL)\nKnowledge of cloud platforms (AWS, GCP, or Azure)\nUnderstanding of microservices architecture',
        'logo': 'https://images.unsplash.com/photo-1572044162444-ad60f128bdea?w=100&h=100&fit=crop',
    },
    {
        'title': 'DevOps Engineer', 'company': 'CloudNine',
        'location': 'Austin, TX', 'type': 'Full-time',
        'salary': '$110,000 – $150,000',
        'description': 'Looking for a DevOps Engineer to manage our infrastructure and deployment pipelines. You will ensure our systems are reliable, scalable, and secure.',
        'requirements': '3+ years of DevOps experience\nStrong knowledge of Docker and Kubernetes\nExperience with CI/CD pipelines\nProficiency in scripting (Bash, Python)\nUnderstanding of infrastructure as code',
        'logo': 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=100&h=100&fit=crop',
    },
    {
        'title': 'Marketing Manager', 'company': 'GrowthLabs',
        'location': 'Los Angeles, CA', 'type': 'Full-time',
        'salary': '$80,000 – $110,000',
        'description': 'We are seeking a creative Marketing Manager to lead our marketing initiatives and drive brand awareness. You will develop comprehensive marketing strategies.',
        'requirements': '5+ years of marketing experience\nStrong understanding of digital marketing\nExperience with analytics tools\nExcellent writing and communication skills\nProven track record of successful campaigns',
        'logo': 'https://images.unsplash.com/photo-1553484771-371a605b060b?w=100&h=100&fit=crop',
    },
    {
        'title': 'Data Scientist', 'company': 'AI Innovations',
        'location': 'Boston, MA', 'type': 'Contract',
        'salary': '$140,000 – $180,000',
        'description': 'Join our data science team to build predictive models and extract insights from large datasets. You will work on cutting-edge machine learning projects.',
        'requirements': 'PhD or Masters in Computer Science, Statistics, or related field\nStrong programming skills in Python or R\nExperience with machine learning frameworks\nKnowledge of statistical analysis\nAbility to communicate complex findings',
        'logo': 'https://images.unsplash.com/photo-1535378620166-273708d44e4c?w=100&h=100&fit=crop',
    },
]

if not Job.objects.exists():
    for data in sample_jobs:
        Job.objects.create(**data)
    print(f'Created {len(sample_jobs)} sample jobs.')
else:
    print('Jobs already exist, skipping seed.')
