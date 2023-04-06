from django.db import models
from django.contrib.auth.models import User # 장고에서 제공하는 기본 유저 사용

# TODO: Profile 모델 생성
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) # 일대일관계
  nickname = models.CharField(max_length=20, null=True)
  image = models.ImageField(upload_to="profile/", null=True)
  class Meta:
    db_table = 'profile' # 장고에서 기본적으로 만들주는 테이블이름 말고 테이블 이름 지정해줌

  def __str__(self):
    return self.nickname