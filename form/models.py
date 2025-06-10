from django.db import models
from django.utils.text import slugify

class CV(models.Model):
    name = models.CharField(max_length=30)
    photo_profile= models.ImageField(blank=True)
    roles = models.CharField(max_length=100)
    location = models.CharField(max_length=30, blank=False)
    email = models.EmailField()
    telp = models.CharField(max_length=30, blank=False)
    web=models.CharField(max_length=30, blank=True)
    summary= models.TextField(max_length=500, blank=False)
    slug= models.SlugField(blank=True, editable=False,max_length=150)
    
    def __str__(self):
        return "{} - {} -{}".format(self.name, self.roles, self.location)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.email}-{self.roles}")
            slug = base_slug
            counter = 1
            while CV.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        self.slug = slug
        super().save(*args, **kwargs)

class Education(models.Model):
    DEGREE_CHOICES = [
        ('SD', 'SD'),
        ('SMP', 'SMP'),
        ('SMA', 'SMA'),
        ('D3','D3'),
        ('S1', 'S1'),
        ('D4','D4'),
        ('S2', 'S2'),
        ('S3','S3'),
    ]
    cv=models.ForeignKey(CV, on_delete=models.CASCADE, related_name='education')
    school_name= models.CharField(max_length=100)
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    grade= models.CharField(max_length=10)
    major= models.CharField(max_length=30)
    location= models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.school_name} ({self.get_degree_display()})"
    
class Skill(models.Model):
    cv= models.ForeignKey(CV, on_delete=models.CASCADE, related_name='skill')
    skill_name= models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.skill_name}"
    
class Certificate(models.Model):
    cv= models.ForeignKey(CV, on_delete=models.CASCADE, related_name='certificate')
    certificate_name= models.CharField(max_length=100)
    year = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    
    def __str__(self):
        return f"{self.certificate_name}"
    
class Experience(models.Model):
    cv= models.ForeignKey(CV, on_delete=models.CASCADE, related_name='experience')
    experience_name= models.CharField(max_length=150)
    location= models.CharField(max_length=30)
    position = models.CharField(max_length=150)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    jobdesc = models.TextField(max_length=1500)
    
    def __str__(self):
        return f"{self.experience_name}"