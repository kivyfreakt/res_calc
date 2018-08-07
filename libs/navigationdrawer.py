# -*- coding: utf-8 -*-
import os

from kivy.animation import Animation
from kivy.properties import StringProperty, ObjectProperty
from kivymd.elevationbehavior import ElevationBehavior
from kivymd.label import MDLabel
from kivymd.list import OneLineIconListItem, ILeftBody, BaseListItem
from kivymd.slidingpanel import SlidingPanel
from kivymd.theming import ThemableBehavior

from kivymd.icon_definitions import md_icons


class NavigationDrawer(SlidingPanel, ThemableBehavior, ElevationBehavior):
    widget_list = ObjectProperty()

    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, BaseListItem):
            self.widget_list.add_widget(widget, index)
            widget.bind(on_release=lambda x: self.toggle())
        else:
            super(NavigationDrawer, self).add_widget(widget, index)

    def _get_main_animation(self, duration, t, x, is_closing):
        a = super(NavigationDrawer, self)._get_main_animation(duration, t, x,
                                                              is_closing)
        a &= Animation(elevation=0 if is_closing else 5, t=t, duration=duration)
        return a


class NDIconLabel(ILeftBody, MDLabel):
    pass


class NavigationDrawerIconButton(OneLineIconListItem):
    icon = StringProperty()

    def on_icon(self, instance, value):
        self.ids['_icon'].text = u"{}".format(md_icons[value])
