from terp.routing import router
from terp.sources import parser
from terp.output import renderer


cache = parser.parse('data')
routed = router.route(cache)
report = renderer.out(routed, 'out')

