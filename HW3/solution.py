from uuid import uuid4
from datetime import datetime
from collections import defaultdict
import math


class User:
    def __init__(self, full_name):
        self.full_name = full_name
        self.uuid = uuid4()
        self.posts = []

    def add_post(self, post_content):
        self.posts = self.posts[-49:]
        self.posts.append(Post(self, post_content))
        return self.posts

    def get_post(self):
        for post in self.posts:
            yield post


class Post:
    def __init__(self, author, content):
        self.author = author.uuid
        self.published_at = datetime.now()
        self.content = content


class SocialGraph:
    def __init__(self):
        self.graph_for_user_uuids = defaultdict(list)
        self.users = defaultdict(User)

    def check_user_exist(self, user_uuid):
        if user_uuid not in self.graph_for_user_uuids:
            raise UserDoesNotExistError

    def add_user(self, user):
        if user.uuid in self.graph_for_user_uuids:
            raise UserAlreadyExistsError()
        else:
            self.graph_for_user_uuids[user.uuid]
            self.users[user.uuid] = user

    def get_user(self, user_uuid):
        self.check_user_exist(user_uuid)
        return self.users[user_uuid]

    def delete_user(self, user_uuid):
        self.check_user_exist(user_uuid)
        del self.users[user_uuid]
        del self.graph_for_user_uuids[user_uuid]

    def follow(self, follower, followee):
        self.check_user_exist(follower)
        self.check_user_exist(followee)
        if follower == followee:
            raise UserCannotFollowHimself
        elif not self.is_following(follower, followee):
            self.graph_for_user_uuids[follower].append(followee)

    def unfollow(self, follower, followee):
        self.check_user_exist(follower)
        self.check_user_exist(followee)
        self.graph_for_user_uuids[follower].remove(followee)

    def is_following(self, follower, followee):
        self.check_user_exist(follower)
        self.check_user_exist(followee)
        if follower == followee:
            raise UserCannotFollowHimself
        if followee in self.graph_for_user_uuids[follower]:
            return True
        return False

    def followers(self, user_uuid):
        self.check_user_exist(user_uuid)
        buffer_set = set()
        for user in self.graph_for_user_uuids:
            if user_uuid in self.graph_for_user_uuids[user]:
                buffer_set.add(user)
        return buffer_set

    def following(self, user_uuid):
        self.check_user_exist(user_uuid)
        return set(self.graph_for_user_uuids[user_uuid])

    def friends(self, user_uuid):
        self.check_user_exist(user_uuid)
        user_followers = self.followers(user_uuid)
        user_following = self.following(user_uuid)
        return user_followers & user_following

    def __find_min_path(self, from_user_uuid, to_user_uuid, path=[]):
        if from_user_uuid == to_user_uuid and path == []:
            return None
        path = path + [from_user_uuid]
        if from_user_uuid == to_user_uuid:
            return path
        if from_user_uuid not in self.graph_for_user_uuids:
            return None
        shortest = None
        for vertex in self.graph_for_user_uuids[from_user_uuid]:
            if vertex not in path:
                newpath = self.__find_min_path(vertex, to_user_uuid, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def max_distance(self, user_uuid):
        self.check_user_exist(user_uuid)
        distances = [0]
        for user in self.graph_for_user_uuids:
            distance = self.__find_min_path(user_uuid, user)
            if distance is not None:
                distances.append(len(distance))

        if distances == [0]:
            return math.inf
        return max(distances) - 1

    def min_distance(self, from_user_uuid, to_user_uuid):
        self.check_user_exist(from_user_uuid)
        self.check_user_exist(to_user_uuid)

        distance = self.__find_min_path(from_user_uuid, to_user_uuid)
        if distance is None:
            raise UsersNotConnectedError
        return len(distance) - 1

    def nth_layer_followings(self, user_uuid, n):
        self.check_user_exist(user_uuid)
        if n == 0:
            return set()
        distances = []
        for user in self.graph_for_user_uuids:
            distance = self.__find_min_path(user_uuid, user)
            if distance is not None:
                distances.append(distance)

        return set([distance[n]
                    for distance in distances if len(distance) == n + 1])

    def generate_feed(self, user_uuid, offset=0, limit=10):
        self.check_user_exist(user_uuid)
        feed = []
        user_following = self.graph_for_user_uuids[user_uuid]
        for user in user_following:
            a = self.users[user].get_post()
            for post in a:
                feed.append(post)

        feed.sort(key=lambda post: post.published_at, reverse=True)

        return feed[offset:(limit + offset)]


class UserDoesNotExistError(Exception):
    def __init__(self):
        self.message = "User does not exist"


class UserAlreadyExistsError(Exception):
    def __init__(self):
        self.message = "User already exist"


class UsersNotConnectedError(Exception):
    def __init__(self):
        self.message = "Users are not connected"


class UserCannotFollowHimself(Exception):
    def __init__(self):
        self.message = "User cannot follow himself"

# maria = User("Maria")
# ivan = User("Ivan")
# pesho = User("Pesho")


# graph = SocialGraph()
# graph.add_user(maria)
# graph.add_user(ivan)
# graph.add_user(pesho)


# graph.follow(maria.uuid, ivan.uuid)

# graph.follow(maria.uuid, pesho.uuid)

# graph.follow(ivan.uuid, pesho.uuid)

# print (graph.nth_layer_followings(maria.uuid, 0))


# terry = User("Terry")
# eric = User("Eric")
# graham = User("Graham")
# john = User("John")
# michael = User("Michael")

# graph = SocialGraph()
# graph.add_user(terry)
# graph.add_user(eric)
# graph.add_user(graham)
# graph.add_user(john)
# graph.add_user(michael)

# graph.follow(terry.uuid, eric.uuid)
# graph.follow(terry.uuid, graham.uuid)
# graph.follow(eric.uuid, michael.uuid)
# graph.follow(eric.uuid, john.uuid)
# graph.follow(john.uuid, graham.uuid)


# print(graph.nth_layer_followings(terry.uuid, 2))
# print(graph._SocialGraph__find_min_path(terry.uuid, graham.uuid))

# graph.follow(terry.uuid, eric.uuid)
# graph.follow(terry.uuid, graham.uuid)
# graph.follow(terry.uuid, john.uuid)
# graph.follow(terry.uuid, michael.uuid)

# for i in range(40):
#     terry.add_post(i)

# for i in range(10):
#     eric.add_post(str(i))
#     sleep(0.000001)
#     graham.add_post(str(10 + i))
#     sleep(0.000001)
#     john.add_post(str(20 + i))
#     sleep(0.000001)
#     michael.add_post(str(30 + i))
#     sleep(0.000001)

# posts = graph.generate_feed(terry.uuid, 500, 10)
# for post in posts:
#     print (post.content)

# zero = User("Zero")
# one = User("one")
# two = User("two")
# three = User("three")
# four = User("four")
# five = User("five")
# six = User("six")
# seven = User("seven")

# graph = SocialGraph()

# graph.add_user(zero)
# graph.add_user(one)
# graph.add_user(two)
# graph.add_user(three)
# graph.add_user(four)
# graph.add_user(five)
# graph.add_user(six)
# graph.add_user(seven)

# graph.follow(zero.uuid, one.uuid)
# graph.follow(zero.uuid, four.uuid)
# graph.follow(one.uuid, two.uuid)
# graph.follow(two.uuid, three.uuid)
# graph.follow(three.uuid, four.uuid)
# graph.follow(four.uuid, five.uuid)
# graph.follow(four.uuid, six.uuid)
# graph.follow(six.uuid, seven.uuid)

# ne = graph.nth_layer_followings(one.uuid, 5)
# print(ne)

# for n in ne:
#     print(graph.users[n].full_name)
