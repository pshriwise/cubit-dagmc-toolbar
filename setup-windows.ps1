$curr_dir=Get-Location
Write-Host "Generating toolbar file for directory: ${curr_dir}"
(Get-Content "$curr_dir\toolbars\template.tmpl") `
    -replace "@DAGMC_TOOLBAR_LOCATION@", "$curr_dir" `
    -replace "/icons/", "\icons\" `
    -replace "/scripts/", "\scripts\" `
    -replace "/scripts", "\scripts" `
    | Set-Content "toolbars\dagmc_toolbar.ttb"