from Core.RedditObjects import User, Subreddit
from Core import Injector
from version import __version__


class ObjectUpdater:

    """
    A class that updates outdated reddit objects that have been loaded from a pickled state to a new version of the
    objects with current methods and attributes that are needed to be used in the current version of the app.
    """

    @classmethod
    def update_user(cls, user):
        """
        Creates a new User object with current methods and attributes and fills in the new users attributes with
        attributes from the old user object.
        :param user: The User object which is to be updated.
        :type user: User
        """
        new_user = User(__version__, user.name, None, user.post_limit, user.avoid_duplicates,
                        user.download_videos, user.download_images, cls.get_nsfw_filter(user), user.name_downloads_by,
                        user.user_added)
        cls.update_extras(user, new_user)
        new_user.object_type = 'USER'
        return new_user

    @classmethod
    def update_subreddit(cls, sub):
        """
        Creates a new Subreddit object with current methods and attributes and fills in the new subs attributes with
        the attributes from the old subreddit object.
        :param sub: The outdated subreddit object wich is to be updated.
        :type sub: Subreddit
        """
        new_sub = Subreddit(__version__, sub.name, None, sub.post_limit, sub.avoid_duplicates,
                            sub.download_videos, sub.download_images, cls.get_nsfw_filter(sub),
                            sub.subreddit_save_method, sub.name_downloads_by, sub.user_added)
        cls.update_extras(sub, new_sub)
        new_sub.object_type = 'SUBREDDIT'
        return new_sub

    @staticmethod
    def get_nsfw_filter(reddit_object):
        """
        Returns the supplied reddit objects nsfw_filter method if the attribute exists and returns the global 
        nsfw_filter if it does not.
        :param reddit_object: The old reddit object.
        :return: The nsfw_filter appropriate for the supplied reddit object
        """
        try:
            return reddit_object.nsfw_filter
        except AttributeError:
            return Injector.get_settings_manager().nsfw_filter

    @classmethod
    def update_extras(cls, old, new):
        """
        Updates any object attributes that do not need to be supplied upon object creation.
        :param old:
        :param new:
        :return:
        """
        new.do_not_edit = old.do_not_edit
        new.date_limit = old.date_limit
        new.custom_date_limit = old.custom_date_limit
        cls.update_save_path(old, new)
        cls.get_previous_downloads(old, new)
        cls.get_saved_content(old, new)
        cls.get_saved_submissions(old, new)
        cls.get_number_of_downloads(old, new)

    @staticmethod
    def update_save_path(old, new):
        """
        Updates the save path for the new reddit object if needed.
        :param old: The old reddit object.
        :param new: The new reddit object.
        """
        if not old.save_path.endswith(old.name) and not old.save_path.endswith('%s/' % old.name):
            new.save_path = old.save_path
        else:
            new.save_path = old.save_path.split(old.name, 1)[0]

    @staticmethod
    def get_previous_downloads(old, new):
        """
        Transfers the previous_downloads list from the old object to the new object.
        :param old: The old reddit object
        :param new: The new reddit object
        :type old: RedditObject
        type new: RedditObject
        """
        try:
            new.previous_downloads = old.previous_downloads
        except AttributeError:
            try:
                new.previous_downloads = old.already_downloaded
            except:
                print('Could not transfer previous downloads')

    @staticmethod
    def get_saved_content(old, new):
        """
        Transfers the saved_content list from the old object to the new object.
        :param old: The old reddit object.
        :param new: The new reddit object.
        :type old: RedditObject
        :type new: RedditObject
        """
        try:
            new.saved_content = old.saved_content
        except AttributeError:
            pass

    @staticmethod
    def get_saved_submissions(old, new):
        """
        Transfers saved submissions for previous reddit object to new reddit object.
        :param old: The old reddit object.
        :param new: The new reddit object.
        :type old: RedditObject
        :type new: RedditObject
        """
        try:
            new.saved_submissions = old.saved_submissions
        except AttributeError:
            pass

    @staticmethod
    def get_number_of_downloads(old, new):
        """
        Transfers number of downloads from previous reddit object to a new reddit object.
        :param old: The old reddit object.
        :param new: The new reddit object.
        :type old: RedditObject
        :type new: RedditObject
        """
        try:
            new.number_of_downloads = old.number_of_downloads
        except AttributeError:
            try:
                new.number_of_downloads = len(old.previous_downloads)
            except:
                pass

    @staticmethod
    def check_settings_manager(settings_manager):
        """
        Checks settings manager attributes for any backwards incompatible changes that may have been made and updates
        the attribute so that it will not cause problems.
        :param settings_manager: The settings manager instance.
        :type settings_manager: SettingsManager
        """
        try:
            int(settings_manager.score_limit_operator)
            settings_manager.score_limit_operator = 'GREATER'
        except ValueError:
            pass
        try:
            int(settings_manager.subreddit_sort_method)
            settings_manager.subreddit_sort_method = 'HOT'
        except ValueError:
            pass
        try:
            int(settings_manager.subreddit_sort_top_method)
            settings_manager.subreddit_sort_top_method = 'DAY'
        except ValueError:
            pass
