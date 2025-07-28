"""
Django management command to import legal processes from HTML files.
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from processes.scrapers import extract_and_save_process


class Command(BaseCommand):
    help = 'Import legal processes from HTML files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--directory',
            type=str,
            help='Directory containing HTML files to process'
        )
        parser.add_argument(
            '--file',
            type=str,
            help='Single HTML file to process'
        )

    def handle(self, *args, **options):
        if options['file']:
            self.process_single_file(options['file'])
        elif options['directory']:
            self.process_directory(options['directory'])
        else:
            self.stdout.write(
                self.style.ERROR('Please provide either --file or --directory argument')
            )

    def process_single_file(self, file_path):
        """Process a single HTML file."""
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File not found: {file_path}')
            )
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            process = extract_and_save_process(html_content)
            
            if process:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully processed: {file_path}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Could not extract process data from: {file_path}')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing {file_path}: {e}')
            )

    def process_directory(self, directory_path):
        """Process all HTML files in a directory."""
        if not os.path.exists(directory_path):
            self.stdout.write(
                self.style.ERROR(f'Directory not found: {directory_path}')
            )
            return

        html_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith('.html'):
                    html_files.append(os.path.join(root, file))

        if not html_files:
            self.stdout.write(
                self.style.WARNING(f'No HTML files found in: {directory_path}')
            )
            return

        self.stdout.write(f'Found {len(html_files)} HTML files to process')

        processed = 0
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()

                process = extract_and_save_process(html_content)
                
                if process:
                    processed += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Processed: {file_path}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Could not extract data from: {file_path}')
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {file_path}: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {processed} out of {len(html_files)} files')
        ) 