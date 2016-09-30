import unittest
import datetime
import math
from time import sleep

import sol2 as s


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = s.User("Lord Bendtner")

    def test_name(self):
        self.assertIsNotNone(getattr(self.user, 'full_name'))
        self.assertEqual(self.user.full_name, "Lord Bendtner")

    def test_has_uuid(self):
        self.assertIsNotNone(getattr(self.user, 'uuid'))

    def test_add_post(self):
        self.user.add_post("I scored a hattrick today!")
        post = next(self.user.get_post())
        self.assertEqual(post.content, "I scored a hattrick today!")
        self.assertEqual(self.user.uuid, post.author)
        self.assertTrue(isinstance(post.published_at, datetime.datetime))

        for i in range(60):
            self.user.add_post(chr(i + 64))
        all_posts = list(self.user.get_post())
        length = len(all_posts)
        self.assertEqual(length, 50)
        self.assertEqual(all_posts[length - 1].content, '{')
        self.assertEqual(all_posts[0].content, 'J')


class TestSocialGraph(unittest.TestCase):
    def setUp(self):
        self.social_graph = s.SocialGraph()
        self.terry = s.User("Terry Gilliam")
        self.eric = s.User("Eric Idle")
        self.graham = s.User("Graham Chapman")
        self.john = s.User("John Cleese")
        self.michael = s.User("Michael Palin")

        self.social_graph.add_user(self.terry)
        self.social_graph.add_user(self.eric)
        self.social_graph.add_user(self.graham)
        self.social_graph.add_user(self.john)
        self.social_graph.add_user(self.michael)

    def test_add_get_del_user(self):
        self.assertTrue(
            self.social_graph.get_user(self.terry.uuid), self.terry)
        self.assertTrue(
            self.social_graph.get_user(self.eric.uuid), self.eric)
        self.assertTrue(
            self.social_graph.get_user(self.graham.uuid), self.graham)
        self.assertTrue(
            self.social_graph.get_user(self.john.uuid), self.john)
        self.assertTrue(
            self.social_graph.get_user(self.michael.uuid), self.michael)

        with self.assertRaises(s.UserAlreadyExistsError):
            self.social_graph.add_user(self.eric)
        with self.assertRaises(s.UserAlreadyExistsError):
            self.social_graph.add_user(self.graham)
        with self.assertRaises(s.UserAlreadyExistsError):
            self.social_graph.add_user(self.john)
        with self.assertRaises(s.UserAlreadyExistsError):
            self.social_graph.add_user(self.michael)
        with self.assertRaises(s.UserAlreadyExistsError):
            self.social_graph.add_user(self.terry)

        self.social_graph.delete_user(self.terry.uuid)
        self.assertTrue(
            self.social_graph.get_user(self.eric.uuid), self.eric)
        with self.assertRaises(s.UserDoesNotExistError):
            self.social_graph.get_user(self.terry.uuid)

    def test_followers_following(self):
        self.social_graph.follow(self.terry.uuid, self.eric.uuid)
        self.social_graph.follow(self.terry.uuid, self.graham.uuid)
        self.social_graph.follow(self.graham.uuid, self.john.uuid)
        self.social_graph.follow(self.michael.uuid, self.terry.uuid)
        self.social_graph.follow(self.eric.uuid, self.terry.uuid)

        with self.assertRaises(ValueError):
            self.social_graph.is_following(self.terry.uuid, self.terry.uuid)
        self.assertTrue(
            self.social_graph.is_following(self.terry.uuid, self.eric.uuid))
        self.assertTrue(
            self.social_graph.is_following(self.terry.uuid, self.graham.uuid))
        self.assertTrue(
            self.social_graph.is_following(self.graham.uuid, self.john.uuid))
        self.assertTrue(
            self.social_graph.is_following(self.michael.uuid, self.terry.uuid))
        self.assertFalse(
            self.social_graph.is_following(self.graham.uuid, self.terry.uuid))

        self.assertEqual(
            self.social_graph.followers(self.terry.uuid),
            {self.eric.uuid, self.michael.uuid})
        self.assertEqual(
            self.social_graph.followers(self.graham.uuid),
            {self.terry.uuid})
        self.assertEqual(
            self.social_graph.followers(self.john.uuid),
            {self.graham.uuid})

        self.assertEqual(
            self.social_graph.following(self.graham.uuid),
            {self.john.uuid})

        self.assertEqual(
            self.social_graph.following(self.michael.uuid),
            {self.terry.uuid})

        self.assertEqual(
            self.social_graph.following(self.eric.uuid),
            {self.terry.uuid})

    def test_friends(self):
        self.social_graph.follow(self.terry.uuid, self.eric.uuid)
        self.social_graph.follow(self.terry.uuid, self.graham.uuid)
        self.social_graph.follow(self.graham.uuid, self.john.uuid)
        self.social_graph.follow(self.graham.uuid, self.terry.uuid)
        self.social_graph.follow(self.john.uuid, self.graham.uuid)
        self.social_graph.follow(self.michael.uuid, self.terry.uuid)
        self.social_graph.follow(self.eric.uuid, self.terry.uuid)

        self.assertEqual(
            self.social_graph.friends(self.terry.uuid),
            {self.eric.uuid, self.graham.uuid})

        self.assertEqual(
            self.social_graph.friends(self.graham.uuid),
            {self.john.uuid, self.terry.uuid})

        self.assertEqual(
            self.social_graph.friends(self.eric.uuid),
            {self.terry.uuid})

        self.assertEqual(
            self.social_graph.friends(self.michael.uuid),
            set())

    # def test_all_paths_1(self):
    #     self.social_graph.follow(self.terry.uuid, self.eric.uuid)
    #     self.social_graph.follow(self.eric.uuid, self.graham.uuid)
    #     self.social_graph.follow(self.graham.uuid, self.john.uuid)
    #     self.social_graph.follow(self.terry.uuid, self.michael.uuid)

    #     a = s.User("A")
    #     b = s.User("B")
    #     c = s.User("C")

    #     self.social_graph.add_user(a)
    #     self.social_graph.add_user(b)
    #     self.social_graph.add_user(c)

    #     self.social_graph.follow(self.michael.uuid, a.uuid)
    #     self.social_graph.follow(a.uuid, b.uuid)
    #     self.social_graph.follow(b.uuid, self.eric.uuid)
    #     self.social_graph.follow(self.eric.uuid, c.uuid)
    #     self.social_graph.follow(c.uuid, self.eric.uuid)

    #     self.assertEqual(
    #         self.social_graph.find_all_paths(self.terry.uuid),
    #         {(self.terry.uuid,
    #             self.eric.uuid,
    #             self.graham.uuid,
    #             self.john.uuid),
    #          (self.terry.uuid,
    #             self.eric.uuid,
    #             c.uuid),
    #          (self.terry.uuid,
    #             self.michael.uuid,
    #             a.uuid,
    #             b.uuid,
    #             self.eric.uuid,
    #             self.graham.uuid,
    #             self.john.uuid),
    #          (self.terry.uuid,
    #             self.michael.uuid,
    #             a.uuid,
    #             b.uuid,
    #             self.eric.uuid,
    #             c.uuid)
    #          })

    # def test_all_paths_2(self):
    #     a = s.User("A")
    #     b = s.User("B")
    #     c = s.User("C")
    #     d = s.User("D")

    #     self.social_graph.add_user(a)
    #     self.social_graph.add_user(b)
    #     self.social_graph.add_user(c)
    #     self.social_graph.add_user(d)

    #     self.social_graph.follow(a.uuid, b.uuid)
    #     self.social_graph.follow(a.uuid, c.uuid)
    #     self.social_graph.follow(b.uuid, c.uuid)
    #     self.social_graph.follow(b.uuid, d.uuid)
    #     self.social_graph.follow(c.uuid, d.uuid)
    #     self.social_graph.follow(d.uuid, c.uuid)

    #     self.assertEqual(
    #         self.social_graph.find_all_paths(a.uuid),
    #         {(a.uuid, b.uuid, c.uuid, d.uuid),
    #          (a.uuid, b.uuid, d.uuid, c.uuid),
    #          (a.uuid, c.uuid, d.uuid)})

    def test_distance(self):
        self.social_graph.follow(self.terry.uuid, self.eric.uuid)
        self.social_graph.follow(self.eric.uuid, self.graham.uuid)
        self.social_graph.follow(self.graham.uuid, self.john.uuid)
        self.social_graph.follow(self.terry.uuid, self.michael.uuid)

        a = s.User("A")
        b = s.User("B")
        c = s.User("C")

        self.social_graph.add_user(a)
        self.social_graph.add_user(b)
        self.social_graph.add_user(c)

        self.social_graph.follow(self.michael.uuid, a.uuid)
        self.social_graph.follow(a.uuid, b.uuid)
        self.social_graph.follow(b.uuid, self.eric.uuid)
        self.social_graph.follow(self.eric.uuid, c.uuid)
        self.social_graph.follow(c.uuid, self.eric.uuid)

        self.assertEqual(
            self.social_graph.max_distance(self.john.uuid), math.inf)
        self.assertEqual(self.social_graph.max_distance(self.terry.uuid), 3)
        self.assertEqual(
            self.social_graph.min_distance(self.terry.uuid, self.eric.uuid), 1)
        self.social_graph.follow(self.michael.uuid, self.terry.uuid)
        self.assertEqual(
            self.social_graph.min_distance(
                self.michael.uuid, self.eric.uuid), 2)

        self.social_graph.unfollow(b.uuid, self.eric.uuid)
        self.assertEqual(self.social_graph.max_distance(self.terry.uuid), 3)
        with self.assertRaises(s.UsersNotConnectedError):
            self.social_graph.min_distance(a.uuid, self.eric.uuid)

    def test_nth_layer_follwings(self):
        self.social_graph.follow(self.terry.uuid, self.graham.uuid)
        self.social_graph.follow(self.john.uuid, self.michael.uuid)
        self.social_graph.follow(self.terry.uuid, self.john.uuid)

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.terry.uuid, 1),
            {self.graham.uuid, self.john.uuid})
        self.assertEqual(
            self.social_graph.nth_layer_followings(self.terry.uuid, 2),
            {self.michael.uuid})
        self.assertEqual(
            self.social_graph.nth_layer_followings(self.graham.uuid, 1),
            set())

    def test_nth_layer_follwings2(self):
        self.social_graph = s.SocialGraph()
        self.zero = s.User("Zero")
        self.one = s.User("One")
        self.two = s.User("Two")
        self.three = s.User("Three")
        self.four = s.User("Four")
        self.five = s.User("Five")
        self.six = s.User("Six")

        self.social_graph.add_user(self.zero)
        self.social_graph.add_user(self.one)
        self.social_graph.add_user(self.two)
        self.social_graph.add_user(self.three)
        self.social_graph.add_user(self.four)
        self.social_graph.add_user(self.five)
        self.social_graph.add_user(self.six)

        self.social_graph.follow(self.zero.uuid, self.one.uuid)
        self.social_graph.follow(self.zero.uuid, self.one.uuid)
        self.social_graph.unfollow(self.zero.uuid, self.one.uuid)
        self.social_graph.follow(self.zero.uuid, self.one.uuid)
        self.social_graph.follow(self.zero.uuid, self.four.uuid)
        self.social_graph.follow(self.zero.uuid, self.five.uuid)
        self.social_graph.follow(self.one.uuid, self.two.uuid)
        self.social_graph.follow(self.one.uuid, self.three.uuid)
        self.social_graph.follow(self.one.uuid, self.four.uuid)
        self.social_graph.follow(self.two.uuid, self.three.uuid)
        self.social_graph.follow(self.four.uuid, self.two.uuid)
        self.social_graph.follow(self.five.uuid, self.six.uuid)
        self.social_graph.follow(self.six.uuid, self.zero.uuid)

        with self.assertRaises(ValueError):
            self.social_graph.nth_layer_followings(self.zero.uuid, -1)

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.zero.uuid, 0),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.zero.uuid, 1),
            {self.one.uuid, self.four.uuid, self.five.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.zero.uuid, 2),
            {self.two.uuid, self.three.uuid, self.six.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.zero.uuid, 3),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.one.uuid, 0),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.one.uuid, 1),
            {self.two.uuid, self.three.uuid, self.four.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.one.uuid, 2),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.two.uuid, 0),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.two.uuid, 1),
            {self.three.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.one.uuid, 2),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.three.uuid, 0),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.three.uuid, 3),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.four.uuid, 0),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.four.uuid, 1),
            {self.two.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.four.uuid, 2),
            {self.three.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.four.uuid, 3),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.five.uuid, 0),
            set())

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.five.uuid, 1),
            {self.six.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.five.uuid, 2),
            {self.zero.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.five.uuid, 3),
            {self.one.uuid, self.four.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.five.uuid, 4),
            {self.two.uuid, self.three.uuid})

        self.assertEqual(
            self.social_graph.nth_layer_followings(self.five.uuid, 5),
            set())

    def test_feed(self):
        self.social_graph.follow(self.terry.uuid, self.eric.uuid)
        self.social_graph.follow(self.terry.uuid, self.graham.uuid)
        self.social_graph.follow(self.terry.uuid, self.john.uuid)
        self.social_graph.follow(self.terry.uuid, self.michael.uuid)
        for i in range(10):
            self.eric.add_post(str(i))
            sleep(0.000001)
            self.graham.add_post(str(10 + i))
            sleep(0.000001)
            self.john.add_post(str(20 + i))
            sleep(0.000001)
            self.michael.add_post(str(30 + i))
            sleep(0.000001)
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 0, 10)],
            ["39", "29", "19", "9", "38", "28", "18", "8", "37", "27"])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 10, 10)],
            ["17", "7", "36", "26", "16", "6", "35", "25", "15", "5"])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 20, 10)],
            ["34", "24", "14", "4", "33", "23", "13", "3", "32", "22"])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 30, 10)],
            ["12", "2", "31", "21", "11", "1", "30", "20", "10", "0"])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 0, 1)],
            ["39"])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 1, 1)],
            ["29"])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 1, 0)],
            [])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 0, 40)],
            ["39", "29", "19", "9", "38", "28", "18", "8", "37", "27",
             "17", "7", "36", "26", "16", "6", "35", "25", "15", "5",
             "34", "24", "14", "4", "33", "23", "13", "3", "32", "22",
             "12", "2", "31", "21", "11", "1", "30", "20", "10", "0"])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 39, 40)],
            ["0"])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 39, 39)],
            ["0"])
        self.assertEqual(
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 10, 140)],
            ["17", "7", "36", "26", "16", "6", "35", "25", "15", "5",
             "34", "24", "14", "4", "33", "23", "13", "3", "32", "22",
             "12", "2", "31", "21", "11", "1", "30", "20", "10", "0"])

        with self.assertRaises(ValueError):
            [post.content
             for post in self.social_graph.generate_feed(self.terry.uuid, 0, -1)]
        with self.assertRaises(ValueError):
            [post.content
        for post in self.social_graph.generate_feed(self.terry.uuid, -1, 10)]

        self.assertEqual([post.content for post in self.eric.get_post()],
                         [str(i) for i in range(10)])
        self.assertEqual([post.content for post in self.graham.get_post()],
                         [str(i) for i in range(10, 20)])
        self.assertEqual([post.content for post in self.john.get_post()],
                         [str(i) for i in range(20, 30)])
        self.assertEqual([post.content for post in self.michael.get_post()],
                         [str(i) for i in range(30, 40)])

if __name__ == "__main__":
    unittest.main()
