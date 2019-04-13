$inpath = $args[0] + "\*.py"

$list = Get-ChildItem $inpath -Recurse
$out = @()
foreach ($i in $list) {
    $out += $i.FullName
}

$out | &'python.exe' .\extract_methoddef_docstring_meta_chinese.py $args[1] $args[2] $args[3] $args[4]