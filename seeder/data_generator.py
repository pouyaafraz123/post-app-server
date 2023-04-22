import random

from controller import user, post, comment
from database.database import get_db
from faker import Faker
from fastapi import Depends, APIRouter
from schema.schemas import UserCreate, UserType, PostCreate, CommentCreate
from sqlalchemy.orm import Session

faker = Faker()

router = APIRouter(
    prefix='/generate',
    tags=['generate']
)


@router.get("/user/{count}", response_model=bool)
def user_generate(count: int, db: Session = Depends(get_db)):
    for i in range(count):
        name = faker.user_name()
        email = faker.email()
        user_exist = user.user_exist_with_username(db, name)
        email_exist = user.user_exist_with_email(db, email)
        if user_exist or email_exist:
            continue
        data = UserCreate(
            email=email,
            username=name,
            password=name,
            type=(
                UserType.SUPER_ADMIN if faker.pybool() else
                UserType.REGULAR)
        )

        user.create_user(db, data)
        print(f"USER: {i} Created.")
    return True


@router.get("/post", response_model=bool)
def post_generate(db: Session = Depends(get_db)):
    users = user.get_all(db)
    for u in users:
        count = faker.pyint() % 5 + 1
        for i in range(count):
            data = PostCreate(
                image_url=random.choice([
                    '''https://s29.picofile.com/file/8461699292/3d_cubes_geometric_neon_3d_background_3840x2160_177.jpg''',
                    '''https://s29.picofile.com/file/8461699300/3d_cubes_colorful_geometric_patterns_4010x2480_906.jpg''',
                    '''https://s29.picofile.com/file/8461699318/10.png''',
                    '''https://s29.picofile.com/file/8461699326/15.jpg''',
                    '''https://s28.picofile.com/file/8461699334/25578.jpg''',
                    '''https://s28.picofile.com/file/8461699342/675592.jpg''',
                    '''https://s28.picofile.com/file/8461699350/6905324.jpg''',
                    '''https://s29.picofile.com/file/8461699368/backiee_76562.jpg''',
                    '''https://s28.picofile.com/file/8461699376/miles_morales_spider_man_minimal_art_marvel_superheroes_3840x4733_5769.png''',
                    '''https://s29.picofile.com/file/8461699384/ipados_14_ipad_air_2020_blue_dark_stock_3840x3840_2909.jpg''',
                    '''https://s28.picofile.com/file/8461699418/macos_monterey_stock_pink_light_layers_5k_8k_7680x7680_5892.jpg''',
                    '''https://s28.picofile.com/file/8461699442/spider_man_marvel_superheroes_marvel_comics_3840x4855_6537.jpg'''
                ]),
                title=faker.paragraph()
            )
            post.create_post(db, data, u["id"])
        print(u["id"])
    return True


@router.get("/comment", response_model=bool)
def comment_generate(db: Session = Depends(get_db)):
    users = user.get_all(db)
    posts = post.get_all(db)

    for p in posts:
        count = faker.pyint() % 50 + 1
        for i in range(count):
            data = CommentCreate(text=faker.paragraph(
                faker.pyint() % 50 + 5))
            random_user = users[faker.pyint() % len(users)]
            comment.create_comment(db, data, random_user["id"], p["id"])
            print(p["id"])
    return True
