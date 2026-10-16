"""Bound screenshot timing claims against pinned official sources and frozen QA."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageChops

R = Path(__file__).resolve().parents[1]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out = R / 'qa/reports/capture118_bounds.json'
    assert not out.exists()
    tree = json.loads((R / 'work/capture118/official_tree_2.1.1.json').read_text('utf-8'))
    entries = {x['path']: x for x in tree['tree']}
    records = json.loads((R / 'work/capture118/source_files_v2.json').read_text('utf-8'))
    for name, local in [('Core/Debugger/LuaApi.cpp', 'work/context107/LuaApi_2.1.1.cpp'),
                        ('Core/NES/NesPpu.cpp', 'work/context107/NesPpu_2.1.1.cpp')]:
        p = R / local
        records.append({'official_path': name, 'local_path': local,
                        'url': 'https://raw.githubusercontent.com/SourMesen/Mesen2/2.1.1/' + name,
                        'sha256': sha(p)})
    for x in records:
        b = (R / x['local_path']).read_bytes()
        git = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        assert git == entries[x['official_path']]['sha']
        assert sha(R / x['local_path']) == x['sha256']
        x['git_blob_sha1'] = git
    assert (R / 'work/capture118/VideoDecoder.cpp').read_bytes() == (R / 'work/context107/VideoDecoder_2.1.1.cpp').read_bytes()
    dec = (R / 'work/capture118/VideoDecoder.cpp').read_text('utf-8')
    wrapper = dec[dec.index('void VideoDecoder::TakeScreenshot(std::stringstream &stream)'):]
    assert 'WaitForAsyncFrameDecode' not in wrapper
    assert '_videoFilter->TakeScreenshot' in wrapper
    ppu = (R / 'work/context107/NesPpu_2.1.1.cpp').read_text('utf-8')
    section = ppu[ppu.index('template<class T> void NesPpu<T>::SendFrame()'):]
    assert section.index('ProcessEvent(EventType::EndFrame)') < section.index('UpdateFrame(frame, forRewind, forRewind)')
    fil = (R / 'work/capture118/BaseVideoFilter.cpp').read_text('utf-8')
    for signature in ['FrameInfo BaseVideoFilter::SendFrame(', 'void BaseVideoFilter::TakeScreenshot(VideoFilterType']:
        body = fil[fil.index(signature):].split('\n}', 1)[0]
        assert '_frameLock.AcquireSafe()' in body
    prev = R / 'qa/reports/cart117_validation_v2.json'
    old = R / 'qa/dialogue/cart115_v6collision047'
    new = R / 'qa/dialogue/cart117_headinghold047'
    prior = json.loads(prev.read_text('utf-8'))
    envs = [json.loads((q / 'environment.json').read_text('utf-8')) for q in [old, new]]
    checked = {}
    exceptions = []
    for x in prior['prefix_PNG_exceptions']:
        n = x['name']; stem = Path(n).stem
        for q, env in zip([old, new], envs):
            for suffix in ['.png', '_ram.bin', '_ppu.bin', '_oam.bin', '_mapping.csv', '_state.txt']:
                p = q / (stem + suffix)
                assert sha(p) == env['files'][p.name]
                checked[p.relative_to(R).as_posix()] = sha(p)
        for suffix in ['_ram.bin', '_ppu.bin', '_oam.bin', '_mapping.csv', '_state.txt']:
            assert (old / (stem + suffix)).read_bytes() == (new / (stem + suffix)).read_bytes()
        a = Image.open(new / n).convert('RGB'); b = Image.open(old / n).convert('RGB')
        diff = ImageChops.difference(a, b)
        pixels = sum(any(c for c in v) for v in diff.getdata())
        assert pixels == x['RGB_different_pixels']
        assert list(diff.getbbox()) == x['RGB_difference_bbox']
        exceptions.append({**x, 'raw_and_core_exact': True, 'exact_rendered_frame_number': None})
    result = {'work': 118, 'status': 'PASS_STATIC_CAPTURE_BOUNDS_NOT_PROVEN_EXCEPTION_CAUSE',
              'official_tag': '2.1.1', 'sources': records,
              'prior117_report_sha256': sha(prev), 'exceptions': exceptions,
              'selected_QA_hashes': checked,
              'facts': {'lua_screenshot_calls_decoder_directly': True,
                        'decoder_screenshot_waits_for_async_decode': False,
                        'NES_endframe_callback_precedes_current_frame_submission': True,
                        'filter_apply_and_screenshot_copy_share_mutex': True},
              'inference': 'EndFrame label alone does not identify the completed filtered frame copied into PNG. Async scheduling is a plausible explanation, not an established cause or measured delay for the three exceptions.',
              'limits': ['Mutex bounds ApplyFilter/copy overlap only; no blanket claim about all downstream rendering or overlays.',
                         'No decoder timeline or published-frame identity was recorded in these PNGs; cannot establish N-1/N-2 or tearing from these artifacts.',
                         'Existing107/111 exact comparisons remain scoped to their measured images; no universal one-frame guarantee.',
                         'Source review and frozen-file recheck only; no emulator run, new CPU case, build/apply, ROM/CSV/config modification or human approval.'],
              'release_eligible': False}
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    print(result['status'], 'official files', len(records), 'selected QA files', len(checked))

if __name__ == '__main__':
    main()
