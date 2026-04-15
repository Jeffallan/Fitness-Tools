import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://jeffallan.github.io',
  base: '/Fitness-Tools',
  integrations: [
    starlight({
      title: 'Fitness Tools',
      description:
        'Python package for health and fitness calculations using ACSM-sourced equations — body composition, rep max estimation, and macronutrient planning.',
      customCss: ['./src/styles/custom.css'],
      head: [
        {
          tag: 'link',
          attrs: {
            rel: 'alternate',
            type: 'text/plain',
            href: '/Fitness-Tools/llms.txt',
            title: 'LLM-friendly content',
          },
        },
      ],
      components: {
        SocialIcons: './src/components/SocialIcons.astro',
        Header: './src/components/Header.astro',
      },
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/Jeffallan/Fitness-Tools',
        },
      ],
      sidebar: [
        { label: 'Home', link: '/' },
        {
          label: 'Getting Started',
          items: [
            { label: 'README', link: '/readme/' },
          ],
        },
        {
          label: 'Python Library',
          autogenerate: { directory: 'library' },
        },
        {
          label: 'Skills',
          autogenerate: { directory: 'skills' },
        },
        {
          label: 'Project',
          items: [
            { label: 'Changelog', link: '/changelog/' },
            { label: 'Contributing', link: '/contributing/' },
          ],
        },
      ],
    }),
  ],
});
