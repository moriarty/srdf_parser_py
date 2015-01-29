from srdf_parser_py.xml_reflection.basics import *
import srdf_parser_py.xml_reflection as xmlr

# Add a 'namespace' for names so that things don't conflict between SRDF and SDF?
# A type registry? How to scope that? Just make a 'global' type pointer?
# Or just qualify names? urdf.geometric, sdf.geometric

xmlr.start_namespace('srdf')


verbose = True

# Common stuff
name_attribute = xmlr.Attribute('name', str)

class Link(xmlr.Object):
  def __init__(self, name = None):
    self.name = name

xmlr.reflect(Link, params = [
   name_attribute
  ])

class Joint(xmlr.Object):
  def __init__(self, name = None): #, value = 0.0):
    self.name = name
    #self.value = value

xmlr.reflect(Joint, params = [
   name_attribute#,
   #xmlr.Attribute('value', float)
  ])


# Common stuff again
link_element = xmlr.Element('link', Link, False)
joint_element = xmlr.Element('joint', Joint, False)

class VirtualJoint(xmlr.Object):
  TYPES = ['unknown', 'fixed', 'floating', 'planar']
  
  def __init__(self, name = None, child_link = None, parent_frame = None, joint_type = None):
    self.name = name
    self.child_link = child_link
    self.parent_frame = parent_frame
    self.type = joint_type
    
  def check_valid(self):
    assert self.type in self.TYPES, "Invalid joint type: {}".format(self.type)
  
  # Aliases
  @property
  def joint_type(self): return self.type
  @joint_type.setter
  def joint_type(self, value): self.type = value

xmlr.reflect(VirtualJoint, params = [
  name_attribute,
  xmlr.Attribute('child_link', str),
  xmlr.Attribute('parent_frame', str),
  xmlr.Attribute('type', str)
  ])


class Chain(xmlr.Object):
  def __init__(self, base_link = None, tip_link = None):
    self.base_link = base_link
    self.tip_link = tip_link

xmlr.reflect(Chain, params = [
  xmlr.Attribute('base_link', str),
  xmlr.Attribute('tip_link', str)
  ])

class EndEffector(xmlr.Object):
  def __init__(self, name = None, group = None, parent_link = None, parent_group = None):
    self.name = name
    self.group = group
    self.parent_link = parent_link
    self.parent_group = parent_group

xmlr.reflect(EndEffector, params = [
  name_attribute,
  xmlr.Attribute('group', str),
  xmlr.Attribute('parent_link', str),
  xmlr.Attribute('parent_group', str)
  ])

class PassiveJoint(xmlr.Object):
  def __init__(self, name = None):
    self.name = name

xmlr.reflect(PassiveJoint, params = [
  name_attribute
  ])

class DisableCollisions(xmlr.Object):
  def __init__(self, link1 = None, link2 = None, reason = None):
    self.link1 = link1
    self.link2 = link2
    self.reason = reason

xmlr.reflect(DisableCollisions, params = [
  xmlr.Attribute('link1', str),
  xmlr.Attribute('link2', str),
  xmlr.Attribute('reason', str)
  ])


class Group(xmlr.Object):
  def __init__(self, name = None, link = None, joint = None, chain = None, group = None):
    self.name = name
    self.link = link
    self.joint = joint
    self.chain = chain

xmlr.reflect(Group, params = [
  name_attribute,
  link_element,
  joint_element,
  xmlr.Element('chain', Chain, False),
  xmlr.Element('group', Group, False)
  ])

class GroupState(xmlr.Object):
  def __init__(self, name = None, joint = None, group = None):
    self.name = name
    self.joint = joint
    self.group = group

xmlr.reflect(GroupState, params = [
  name_attribute,
  joint_element,
  xmlr.Attribute('group', str)
  ])
  
class Robot(xmlr.Object):
  def __init__(self, name = None):
    self.aggregate_init()
    
    self.name = name
    self.groups = []
    self.group_states = []
    self.links = []
    self.joints = []
    self.chains = []
    self.end_effectors = []
    self.virtual_joints = []
    self.disabled_collisions = []
    self.passive_joints = []
    self.group_map = {}
    self.group_state_map = {}
    self.parent_map = {}
    self.child_map = {}
    
  def add_aggregate(self, typeName, elem):
    xmlr.Object.add_aggregate(self, typeName, elem)
    
    if typeName == 'group':
      group = elem
      self.group_map[group.name] = group
    elif typeName == 'group_state':
      group_state = elem
      self.group_state_map[group_state.name] = group_state

  def add_link(self, link):
    self.add_aggregate('link', link)

  def add_joint(self, joint):
    self.add_aggregate('joint', joint)
  
  def add_chain(self, chain):
    self.add_aggregate('chain', chain)
  
  def add_group(self, group):
    self.add_aggregate('group', group)

  @classmethod
  def from_parameter_server(cls, key = 'robot_description_semantic'):
    """
    Retrieve the robot model on the parameter server
    and parse it to create a SRDF robot structure.

    Warning: this requires roscore to be running.
    """
    # Could move this into xml_reflection
    import rospy
    return cls.from_xml_string(rospy.get_param(key))
  
xmlr.reflect(Robot, tag = 'robot', params = [
#   name_attribute,
  xmlr.Attribute('name', str, False), # Is 'name' a required attribute?
  xmlr.AggregateElement('group', Group),
  xmlr.AggregateElement('group_state', GroupState),
  xmlr.AggregateElement('end_effector', EndEffector),
  xmlr.AggregateElement('virtual_joint', VirtualJoint),
  xmlr.AggregateElement('disable_collisions', DisableCollisions)
  ])

# Make an alias
SRDF = Robot

xmlr.end_namespace()
