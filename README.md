# Trouble Shooting

## Requirements

- Python > 3.6

## Installation

```
pip install -r requirements.txt
```

## Pillow를 사용한 이미지 리사이즈

**`member.models.User`**

`save()`메서드와 `_save_thumbnail_process()`메서드 참조.

## 유저 생성 Serailizer의 구현 및 테스트

유저 타입이 Django, Facebook, Google등으로 나누어진다고 가정하고, Django유저로 가입할 때는 `email`필드가 주어졌을 경우 해당 값을 `username`필드에 똑같이 삽입.

이 때, `username`이 이미 `email`에 주어진 값인 유저가 존재하면 예외를 발생시킨다.

**`member.serializers.DjangoUserCreationSerializer`**

`ReadOnlyField()`와 `write_only=True`옵션을 참고.

**`member.apis.DjangoUserCreateView`**

`serializer_class`를 사용해서 유효성 검증 로직은 해당 Serializer class에서 전부 작동함을 확인.

**`member.tests.SignupTest`**

간단한 테스트. 이정도 테스트는 Postman으로 작성하고서 반드시 테스트코드도 작성!
