<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

/*
|--------------------------------------------------------------------------
| Find Unused Translations
|--------------------------------------------------------------------------
|
| This command can be useful in large projects where it's hard to manually
| track which translations are being used and which are not. By running this
| command, developers can easily find and remove unused translations, which
| can help to keep the codebase clean and efficient.
|
*/
class FindUnusedTranslations extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'translations:find-unused {name?}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Finds all unused translations.';

    protected Carbon $start;

    protected ?string $mode = null;

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle(): int
    {
        $this->showBanner('Start');

        $this->start = Carbon::now();
        $this->mode = $this->argument('name');

        // Get translations aka "group keys."
        $translations = $this->getTranslations();

        // Sort translations.
        sort($translations);

        // 1691 translations found.
        $this->info(count($translations) . ' translations found.');
        $this->warn(print_r($translations, true));
        $this->outputBenchmark();

        // Searching for unused translations...
        $this->info('Searching for unused translations...' . "\n");

        $unusedTranslations = $this->findUnusedTranslations($translations);

        // Output all unused translations.
        $this->info('Unused translations found: ' . count($unusedTranslations));
        $this->warn(print_r($unusedTranslations, true));

        $this->outputBenchmark();
        $this->showBanner('End');

        return 0;
    }

    /**
     * Gets translations.
     * Note: If mode is set, only that mode is returned.
     *
     * @return array
     */
    protected function getTranslations(): array
    {
        if ($this->mode !== null) {
            $translations[0] = $this->mode;
        } else {
            $translations = $this->getAllTranslations();
        }

        return $translations;
    }

    /**
     * @return array
     */
    protected function getAllTranslations(): array
    {
        $allTranslations = [];
        $translationValuesDir = 'resources/lang/en';
        $translationValues = [];

        $this->info('Getting all translation from ' . $translationValuesDir . '...');

        // Get all PHP files in the directory
        $files = glob($translationValuesDir . '/*.php');

        foreach ($files as $file) {

            // Remove validation as we want to keep those.
            if (Str::contains($file, ['validation.php', 'auth.php'])) {
                continue;
            }

            // Get the file name without extension
            $group = pathinfo($file, PATHINFO_FILENAME);

            // Require the file and merge the array with the existing translations
            $translationValues[$group] = require $file;
        }

        foreach ($translationValues as $group => $groupKey) {
            foreach ($groupKey as $key => $translationValue) {
                if (is_array($translationValue)) {
                    foreach ($translationValue as $subKey => $subValue) {
                        $allTranslations[] = $group . '.' . $key . '.' . $subKey;
                    }
                } else {
                    $allTranslations[] = $group . '.' . $key;
                }
            }
        }

        return $allTranslations;
    }

    /**
     * This function searches a directory for a translation value. Returns true if found, false if not.
     *
     * @param $dir
     * @param $translationValue
     * @return bool
     */
    protected function searchDirForTranslation($dir, $translationValue): bool
    {
        $command = "grep -rnw '" . $dir . "' -e '" . $translationValue . "'";
        $output = shell_exec($command);

        return !empty($output);
    }

    protected function outputBenchmark(): void
    {
        $this->info("\n".'Execution Time: ' . $this->formatDuration($this->start->diffInSeconds(Carbon::now())) . '.');
    }

    /**
     * @return array
     */
    protected function getDirectories(): array
    {
        return ['app/', 'resources/views/'];
    }

    /**
     * Checks if all values in the found array are false.
     *
     * @param array $found
     * @return bool
     */
    protected function isNotFound(array $found): bool
    {
        return array_reduce($found, function ($carry, $item) {
            return $carry && !$item;
        }, true);
    }

    /**
     * Searches directories for translations.
     *
     * @param $translation
     * @return array
     */
    protected function searchDirectoriesForTranslations($translation): array
    {
        $found = [];
        $this->info("\n".'Searching for ' . $translation);

        foreach ($this->getDirectories() as $dir) {
            $this->info('Directory: ' . $dir);
            $found[$dir] = $this->searchDirForTranslation($dir, $translation);

            if (!$found[$dir]) {
                $this->error("\t".'Not found in ' . $dir . '.');
            } else {
                $this->warn("\t".'Found in ' . $dir . '.');
            }
        }

        return $found;
    }

    /**
     * @param array $translations
     * @return array
     */
    protected function findUnusedTranslations(array $translations): array
    {
        $unusedTranslations = [];
        $this->info('Searching for unused translations...');

        foreach ($translations as $translation) {
            $found = $this->searchDirectoriesForTranslations($translation);

            if ($this->isNotFound($found)) {
                $unusedTranslations[] = $translation;
            }
        }

        return $unusedTranslations;
    }

    protected function showBanner(string $message): void
    {
        $this->info('# '.$message.' Program # - ' . $this->localDatetime(Carbon::now()->format('Y-m-d H:i:s')));
    }
    
    /**
     * Converts integer seconds into a readable string.
     *
     * @param int seconds
     * @return string
     */
    protected function formatDuration(int $seconds) : string
    {
        $hr = 0;
        $min = 0;
    
        if ($seconds < 60) {
            $sec = $seconds;
        } elseif ($seconds < 3600) {
            $min = floor($seconds / 60);
            $sec = $seconds % 60;
        } else {
            $hr = floor($seconds / 3600);
            if ($seconds % 3600 < 60) {
                $sec = $seconds % 3600;
            } else {
                $min = floor(($seconds % 3600) / 60);
                $sec = ($seconds % 3600) % 60;
            }
        }
    
        // Prepend hr if necessary
        $hr = $hr > 0 ? $hr . 'h ' : '';
    
        return $hr . $min . 'm ' . $sec . 's';
    }

    /**
     * Converts datetime to UTC to local time.
     *
     * @param $datetime
     * @param string $format
     * @param string|null $timezone
     * @return string
     */
    protected function localDatetime($datetime = null, string $format = 'LLL', string $timezone = null): string
    {
        if (!$datetime instanceof Carbon) {
            if ($datetime === null) {
                $datetime = Carbon::now();
            } else {
                $datetime = Carbon::parse($datetime);
            }
        }

        $timezone = $timezone ?? config('site.dates_timezone');
        $datetime->setTimezone($timezone);

        // If datetime format type ISO starts w/ an L output it w/ the isoFormat() method, otherwise output in the literal
        // PHP date format.
        $carbonIsoFormats = array_keys(Carbon::now()->getIsoFormats(config('app.locale')));

        if (in_array($format, $carbonIsoFormats)) {
            return $datetime->isoFormat($format);
        } else {
            return $datetime->format($format);
        }
    }
}
