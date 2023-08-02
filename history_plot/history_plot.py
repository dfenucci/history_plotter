import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from .curlyBrace.curlyBrace import curlyBrace
from .date_utils import *
import textwrap
import itertools
import copy

# **********************************************************************************************************************
# *                                                 Graphic utilities                                                  *
# **********************************************************************************************************************
def label_dist(ax, prev_x, prev_y, cur_x, cur_y, angle):
  ratio = 182.5 / np.diff(ax.get_xlim())[0]
  angle = np.deg2rad(angle)
  return (cur_x - prev_x) * ratio * np.sin(angle) + (prev_y - cur_y) * np.cos(angle)

def overlapping_bbox(ax, bboxes, cur_box, inclination=0, y0=0, min_label_dist=2):
  return list(filter(lambda prev_box: (prev_box.x1 > cur_box.x0) and
                                      (label_dist(ax, prev_box.x1, prev_box.y0, cur_box.x1, y0, inclination) < min_label_dist), bboxes))

# Text legend handler
class TextHandler:
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
      width, height = handlebox.width, handlebox.height
      h = copy.copy(orig_handle)
      h.set_position((width/2., height/2.))
      h.set_transform(handlebox.get_transform())
      h.set_ha("center"); h.set_va("center")
      handlebox.add_artist(h)
      return h

# **********************************************************************************************************************
# *                                                    History plot                                                    *
# **********************************************************************************************************************
class HistoryPlotter(object):
  # Static variables
  __brace_spacing = 0.2
  __brace_x = -np.inf
  __group_map = {}
  __bar_height = 2

# private:
  def __bar_y(self):
    return -HistoryPlotter.__bar_height/2 + self.__y_counter

# public:
  def resize(self):
    self.__ax.set_ylim(self.__y_counter-2, 1)
    self.__fig.set_figheight(abs(self.__y_counter-2)/9.5)

  def __init__(self, title, beginning, end=0, interval=100, debug=False):
    self.__fig = plt.figure(); self.__fig.set_figwidth(15)
    self.__ax = plt.gca()
    self.__beginning = beginning
    self.__end = end
    self.__interval = interval
    self.__time_0 = beginning-interval/4
    self.__time_end = end+interval/4
    self.__y_counter = 0
    self.__figname = title
    self.__debug = debug

    # Title
    self.__ax.set_title(title, fontsize=16, va='bottom', pad=25)

    # Set time axis
    self.__ax.set_xlim(beginning-interval/2, end+interval/2)
    self.__ax.set_xticks(range(beginning, end+interval, interval),[year_to_string(y) for y in range(beginning, end+interval, interval)])
    self.__ax.xaxis.tick_top()
    self.__ax.set_yticks([]); self.__ax.set_ylim(auto=True)

    self.__ax.spines['right'].set_visible(False)
    self.__ax.spines['left'].set_visible(False)
    self.__ax.spines['bottom'].set_visible(False)
    self.__ax.spines['top'].set_position(('data', 0))
    self.__ax.grid(axis='x', which='major', color='#D3D3D3', linewidth=0.5)
    self.__current_section_color = '#1F77B4'
    self.__current_subsection_color = None

  def section(self, title, color=None):
    self.__current_subsection_color = None  # Reset subsection color
    if color is not None:
      self.__current_section_color = color
    self.__y_counter -= 4
    self.__ax.text((self.__beginning+self.__end)/2, self.__y_counter, title,
            fontsize='12', ha='center', va='center', backgroundcolor='white')
    self.__y_counter -= 1
    self.resize()

  def subsection(self, title, color=None):
    if color is not None:
      self.__current_subsection_color = color
    self.__y_counter -= 3
    self.__ax.text((self.__beginning+self.__end)/2, self.__y_counter, title,
            fontsize='10', ha='center', va='center', backgroundcolor='white')
    self.__y_counter -= 1
    self.resize()

  def plot_timeline(self, interval_events=None, instant_events=None, event_label_rotation=0):
    # Plot line
    self.__y_counter -= 5
    event_color = self.__current_subsection_color or self.__current_section_color
    time_y = self.__y_counter
    self.__ax.plot([self.__time_0, self.__time_end], [time_y, time_y],
                   'k', linewidth=1, zorder=-5)

    # Plot instant events
    if instant_events is not None:
      min_dx = 25; max_dy = 2.5; inclination = event_label_rotation
      instant_events.sort(key=lambda ie: ie[0])
      y_ann_base = time_y - 4.5
      ann = []
      for year, event in instant_events:
        self.__ax.scatter(year, time_y, c=event_color, zorder=15)
        ann.append(self.__ax.annotate('\n'.join(textwrap.wrap('%s (%s)' % (event, year_to_string(year)), 100)),
                                      xy=(year, time_y), xytext=(year, y_ann_base),
                                      arrowprops=dict(arrowstyle="-", relpos=(1., 1.), shrinkA=0, shrinkB=0),
                                      fontsize=8, va='top', ha='right', linespacing=0.9, rotation = inclination))
      self.resize(); plt.draw()
      textboxes = [ a.get_window_extent().transformed(self.__ax.transData.inverted()) for a in ann ]

      # !! DEBUG !!
      if self.__debug:
        for box in textboxes:
            self.__ax.add_patch( patches.Rectangle((box.x0, box.y0), box.width, box.height, ec='blue', fc='none'))

      for i in range(len(textboxes)):
        cur_box = textboxes[i]
        new_y0 = y_ann_base
        if i:
          cur_box_height = y_ann_base-cur_box.y0
          # Get y0 and x1 coords of overlapping boxes
          y_overlaps = [ label_dist(self.__ax, box.x1, box.y0, cur_box.x1, y_ann_base, inclination)
                           for box in overlapping_bbox(self.__ax, textboxes[0:i], cur_box, y0=y_ann_base, inclination=inclination) ]
          if len(y_overlaps) > 0:
            new_y0 = y_ann_base - (2-min(y_overlaps)) / np.cos(np.deg2rad(inclination))
            ann[i].set_y(new_y0)

        textboxes[i] = transforms.Bbox([[cur_box.x0, new_y0], [cur_box.x1, cur_box.y1]])

      # !! DEBUG !!
      if self.__debug:
        textboxes = [ a.get_window_extent().transformed(self.__ax.transData.inverted()) for a in ann ]
        for box in textboxes:
          self.__ax.add_patch( patches.Rectangle((box.x0, box.y0), box.width, box.height, ec='red', fc='none'))

      self.__y_counter -= max([ box.height for box in [ a.get_window_extent().transformed(self.__ax.transData.inverted()) for a in ann ] ]) - 1

    # Plot interval events
    if interval_events is not None and isinstance(interval_events, list) and len(interval_events):
      y_coord = -HistoryPlotter.__bar_height/2 + time_y
      bar_height = HistoryPlotter.__bar_height
      # Remove timeline behind the bar
      self.__ax.plot(np.array(list(map(lambda t : [max(t[0], self.__time_0), min(t[1], self.__time_end)],
                                       interval_events))).transpose(),
                     [time_y, time_y], 'w', zorder=-2)
      self.__ax.broken_barh(list(map(lambda t : (max(t[0], self.__time_0),
                                                 min(t[1], self.__time_end)-max(t[0], self.__time_0)),
                                     interval_events)), (y_coord, bar_height),
                            facecolors=(event_color), ec=event_color, zorder=10, alpha=0.5)

      # Plot text labels
      seq_idx = sorted(range(len(interval_events)), key=interval_events.__getitem__)
      txt = []; labels = []
      for i,j in zip(range(len(interval_events)), seq_idx):
        txt.append(self.__ax.text((max(interval_events[j][0], self.__time_0)+min(interval_events[j][1], self.__time_end))/2, y_coord + bar_height + 1,
                   '%s' % str(i+1), fontsize=8, ha='center', va='bottom'))
        labels.append('%s (%s)' % (interval_events[j][2], year_interval_to_string(interval_events[j][0], interval_events[j][1])))

      # Plot legend
      self.__y_counter -= 3
      ncol = 3
      leg = self.__ax.legend(itertools.chain(*[txt[i::ncol] for i in range(ncol)]), itertools.chain(*[labels[i::ncol] for i in range(ncol)]),
                            handler_map={plt.Text: TextHandler()}, mode = "expand", ncol = ncol, loc='upper left',
                            bbox_to_anchor=(self.__beginning-self.__interval/2., self.__y_counter, self.__end-self.__beginning+self.__interval, 0),
                            bbox_transform=self.__ax.transData)
      self.__ax.add_artist(leg)
      plt.draw()

      leg_height = leg.get_frame().get_bbox().transformed(self.__ax.transData.inverted()).height

      # !! DEBUG !!
      if self.__debug:
        self.__ax.plot([-800, -800], [self.__y_counter, self.__y_counter - leg_height], 'ro-')

      self.__y_counter -= leg_height + 1

    self.resize()

  def plot_life_bar(self, birth, death, name, group=None):
    if self.__current_section_color is None:
      raise Exception('Life bar must be part of a section, create a section first with new_section')

    # Decrease the counter
    self.__y_counter -= 3

    # Make inputs homogeneous
    if np.isscalar(birth):
        birth_lab = year_to_string(birth)
        birth = (birth, birth)
    else:
        birth_lab = year_interval_to_string(birth[0], birth[1])
    if np.isscalar(death):
        death_lab = year_to_string(death)
        death = (death, death)
    else:
        death_lab = year_interval_to_string(death[0], death[1])

    # Define constants
    text_spacing = 5
    bar_height = HistoryPlotter.__bar_height
    bar_color = self.__current_subsection_color or self.__current_section_color

    # Plot life bar
    life = death[0] - birth[1]
    y_coord = self.__bar_y()
    self.__ax.barh(y_coord, birth[1]-birth[0], height=bar_height, left=birth[0], fc='white', ec=bar_color,
                   hatch='///////', zorder=11, align='edge')
    self.__ax.broken_barh([(birth[0], birth[1]-birth[0]), (birth[1], life), (death[0], death[1]-death[0])], (y_coord, bar_height),
                          fc =('white', bar_color, 'white'), ec=bar_color, hatch='///////', zorder=10)
    self.__ax.text(birth[0]-text_spacing, self.__y_counter, '%s (%s, %s)' % (name, birth_lab, death_lab),
                   fontsize='10', ha='right', va='center', backgroundcolor='white')

    # Store group info
    HistoryPlotter.__brace_x = max(HistoryPlotter.__brace_x, death[1]+20)
    if group is not None:
        if group not in HistoryPlotter.__group_map:
            HistoryPlotter.__group_map[group] = [ y_coord - HistoryPlotter.__brace_spacing,
                                                  y_coord + bar_height + HistoryPlotter.__brace_spacing ]
        else:
            HistoryPlotter.__group_map[group] = [ min(y_coord - HistoryPlotter.__brace_spacing, HistoryPlotter.__group_map[group][0]),
                                                  max(y_coord + bar_height + HistoryPlotter.__brace_spacing, HistoryPlotter.__group_map[group][1])]
    self.resize()

  def plot_groups(self):
    x_coord = HistoryPlotter.__brace_x
    for group, lims in HistoryPlotter.__group_map.items():
        curlyBrace(self.__fig, self.__ax, [x_coord, lims[1]], [x_coord, lims[0]], k_r=1/(lims[1]-lims[0]), color='k')
        self.__ax.text(x_coord+15, sum(lims)/2, group, fontsize='10', ha='left', va='center', backgroundcolor='white')

    # Reset variables
    HistoryPlotter.__brace_x = -np.inf
    HistoryPlotter.__group_map = {}

  def save(self):
    self.__fig.savefig(self.__figname + '.pdf')
    self.__fig.savefig(self.__figname + '.png')

  def show(self):
    self.resize()
    self.save()
    plt.show()
