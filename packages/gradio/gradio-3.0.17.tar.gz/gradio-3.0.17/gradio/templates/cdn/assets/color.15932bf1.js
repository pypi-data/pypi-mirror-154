import { aa as ordered_colors } from './index.66821d9a.js';

const get_next_color = (index) => {
  return ordered_colors[index % ordered_colors.length];
};

export { get_next_color as g };
