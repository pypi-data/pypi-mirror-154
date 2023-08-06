from aiohttp import hdrs
from ..representor import wstljson, cj, nvpjson, xwwwformurlencoded
from urllib.parse import urlencode
from typing import TYPE_CHECKING
from .microservicetestcase import MicroserviceTestCase
from .. import jsonschemavalidator
import logging


if TYPE_CHECKING:
    _Base = MicroserviceTestCase
else:
    _Base = object


class PostMixin(_Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_post(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        json=self._body_post,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual('201: Created', await obj.text())

    async def test_post_nvpjson(self) -> None:
        if self._body_post is not None:
            obj = await self.client.request('POST',
                                            (self._href / '').path,
                                            json=cj.to_nvpjson(self._body_post),
                                            headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
            self.assertEqual('201: Created', await obj.text())
        else:
            self.skipTest('_body_post not defined')

    async def test_post_xwwwformurlencoded(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        try:
            data_ = self._post_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_post cannot be converted xwwwformurlencoded form')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        data=data_,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual('201: Created', await obj.text())

    async def test_post_status(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        json=self._body_post,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(201, obj.status)

    async def test_post_status_nvpjson(self) -> None:
        if self._body_post is not None:
            obj = await self.client.request('POST',
                                            (self._href / '').path,
                                            json=cj.to_nvpjson(self._body_post),
                                            headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
            self.assertEqual(201, obj.status)
        else:
            self.skipTest('_body_post not defined')

    async def test_post_status_xwwwformurlencoded(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        try:
            data_ = self._post_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_post cannot be converted xwwwformurlencoded form')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        data=data_,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(201, obj.status)

    async def test_post_status_empty_body(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_post_status_empty_body_nvpjson(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_post_status_empty_body_xwwwformurlencoded(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_post_status_invalid_type(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        await self._test_invalid({'type': 'foo.bar'})

    async def test_invalid_url(self) -> None:
        if not self._body_post:
            self.skipTest('_body_post not defined')
        obj = await self.client.request('POST',
                                        (self._href / '1').path,
                                        json=self._body_post,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(405, obj.status)

    async def _test_invalid(self, changes) -> None:
        assert self._body_post is not None
        changed = _copy_heaobject_dict_with(cj.to_nvpjson(self._body_post), changes)
        obj = await self.client.request('POST',
                                        (self._href / '').path,
                                        json=changed,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    def _post_data(self):
        return _to_xwwwformurlencoded_data(self._body_post)


class PutMixin(_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_put(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=self._body_put,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual('', await obj.text())

    async def test_put_nvpjson(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=cj.to_nvpjson(self._body_put) if self._body_put is not None else None,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual('', await obj.text())

    async def test_put_xwwwformurlencoded(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        try:
            data_ = self._put_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_put cannot be converted xwwwformurlencoded form')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            data=data_,
                                            headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
            self.assertEqual('', await obj.text())

    async def test_put_status(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=self._body_put,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(204, obj.status)

    async def test_put_status_wrong_format(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            json=cj.to_nvpjson(self._body_put),
                                            headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
            self.assertEqual(400, obj.status)

    async def test_put_status_nvpjson(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            json=cj.to_nvpjson(self._body_put),
                                            headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
            self.assertEqual(204, obj.status)

    async def test_put_status_nvpjson_wrong_format(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        try:
            data_ = self._put_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_put cannot be converted xwwwformurlencoded form')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            json=data_,
                                            headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_xwwwformurlencoded(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        try:
            data_ = self._put_data()
        except jsonschemavalidator.ValidationError:
            self.skipTest('_body_put cannot be converted xwwwformurlencoded form')
        else:
            obj = await self.client.request('PUT',
                                            (self._href / self._id()).path,
                                            data=data_,
                                            headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
            self.assertEqual(204, obj.status)

    async def test_put_status_xwwwformurlencoded_wrong_format(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=self._body_put,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_empty_body(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / '1').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_empty_body_nvpjson(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / '1').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_empty_body_xwwwformurlencoded(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        obj = await self.client.request('PUT',
                                        (self._href / '1').path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: xwwwformurlencoded.MIME_TYPE})
        self.assertEqual(400, obj.status)

    async def test_put_status_missing_id(self) -> None:
        obj = await self.client.request('PUT',
                                        self._href.path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: cj.MIME_TYPE})
        self.assertEqual(405, obj.status)

    async def test_put_status_missing_id_nvpjson(self) -> None:
        obj = await self.client.request('PUT',
                                        self._href.path,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(405, obj.status)

    async def test_put_status_invalid_type(self) -> None:
        if not self._body_put:
            self.skipTest('_body_put not defined')
        await self._test_invalid({'type': 'foo.bar'})

    async def test_put_content(self) -> None:
        if self._put_content_status is None:
            self.skipTest('_put_content_status not defined')
        if self._content_id is None:
            self.skipTest('_content_id not defined')
        obj = await self.client.request('PUT',
                                        (self._href / self._content_id / 'content').path,
                                        data='The quick brown fox jumps over the lazy dog',
                                        headers={**self._headers, hdrs.CONTENT_TYPE: 'text/plain'})
        self.assertEquals(self._put_content_status, obj.status)

    async def _test_invalid(self, changes) -> None:
        changed = _copy_heaobject_dict_with(self._body_put, changes)
        obj = await self.client.request('PUT',
                                        (self._href / self._id()).path,
                                        json=changed,
                                        headers={**self._headers, hdrs.CONTENT_TYPE: nvpjson.MIME_TYPE})
        self.assertEqual(400, obj.status)

    def _put_data(self):
        return _to_xwwwformurlencoded_data(self._body_put)

    def _id(self):
        logging.getLogger(__name__).debug('Template is %s', self._body_put)
        for e in self._body_put['template']['data']:
            if e['name'] == 'id':
                return e.get('value')


class GetOneMixin(_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_get(self) -> None:
        print(self._expected_one)
        obj = await self.client.request('GET',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        self.assertEqual(_ordered(self._expected_one), _ordered(await obj.json()))

    async def test_get_status(self) -> None:
        obj = await self.client.request('GET',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_get_wstl(self) -> None:
        if not self._expected_one_wstl:
            self.skipTest('self._expected_one_wstl is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id()).path,
                                        headers={**self._headers, hdrs.ACCEPT: wstljson.MIME_TYPE})
        self.assertEqual(_ordered(self._expected_one_wstl), _ordered(await obj.json()))

    async def test_get_not_acceptable(self) -> None:
        if not self._expected_one_wstl:
            self.skipTest('self._expected_one_wstl is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id()).path,
                                        headers={**self._headers, hdrs.ACCEPT: 'application/msword'})
        self.assertEqual(406, obj.status)

    async def test_get_duplicate_form(self) -> None:
        if not self._expected_one_duplicate_form:
            self.skipTest('self._expected_one_duplicate_wstl is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id() / 'duplicator').path,
                                        headers=self._headers)
        self.assertEqual(_ordered(self._expected_one_duplicate_form), _ordered(await obj.json()))

    async def test_opener_header(self) -> None:
        if not self._expected_opener:
            self.skipTest('self._expected_opener is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id() / 'opener').path,
                                        headers=self._headers)
        self.assertEqual(self._expected_opener, obj.headers[hdrs.LOCATION])

    async def test_opener_body(self) -> None:
        if not self._expected_opener_body:
            self.skipTest('self._expected_opener_body is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id() / 'opener').path,
                                        headers=self._headers)
        self.assertEqual(_ordered(self._expected_opener_body), _ordered(await obj.json()))

    async def test_get_content(self) -> None:
        if not self._content:
            self.skipTest('self._content is not defined')
            return
        if not self._coll:
            self.skipTest('self._coll is not defined')
            return
        async with self.client.request('GET',
                                        (self._href / self._id() / 'content').path,
                                        headers=self._headers) as resp:
            expected = self._content[self._coll][self._id()]
            if isinstance(expected, (dict, list)):
                self.assertEqual(_ordered(expected), _ordered(await resp.json()))
            elif isinstance(expected, str):
                self.assertEqual(expected, await resp.text())
            else:
                self.assertEqual(expected, await resp.read())

    async def test_get_content_type(self) -> None:
        if not self._content:
            self.skipTest('self._content is not defined')
        if not self._content_type:
            self.skipTest('self._content_type is not defined')
        obj = await self.client.request('GET',
                                        (self._href / self._id() / 'content').path,
                                        headers=self._headers)
        flag = True
        try:
            self.assertEqual(self._content_type, obj.headers.get(hdrs.CONTENT_TYPE))
            obj.close()
            flag = False
        finally:
            if flag:
                try:
                    obj.close()
                except OSError:
                    pass

    def _id(self):
        logging.getLogger(__name__).debug('Collection is %s', self._body_put)
        for e in self._expected_one[0]['collection']['items'][0]['data']:
            if e['name'] == 'id':
                return e.get('value')



class GetAllMixin(_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_get_all(self) -> None:
        obj = await self.client.request('GET',
                                        (self._href / '').path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_get_all_json(self) -> None:
        obj = await self.client.request('GET',
                                        (self._href / '').path,
                                        headers=self._headers)
        self.assertEqual(_ordered(self._expected_all), _ordered(await obj.json()))

    async def test_get_all_wstl(self) -> None:
        if not self._expected_all_wstl:
            self.skipTest('self._expected_all_wstl is not defined')
        obj = await self.client.request('GET',
                                        (self._href / '').path,
                                        headers={**self._headers, hdrs.ACCEPT: wstljson.MIME_TYPE})
        self.assertEqual(_ordered(self._expected_all_wstl), _ordered(await obj.json()))


class DeleteMixin(_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def test_delete_success(self) -> None:
        obj = await self.client.request('DELETE',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        self.assertEqual(204, obj.status)

    async def test_delete_fail(self) -> None:
        obj = await self.client.request('DELETE',
                                        (self._href / '3').path,
                                        headers=self._headers)
        self.assertEqual(404, obj.status)

    def _id(self):
        logging.getLogger(__name__).debug('Collection is %s', self._body_put)
        for e in self._expected_one[0]['collection']['items'][0]['data']:
            if e['name'] == 'id':
                return e.get('value')


def _copy_heaobject_dict_with(d, changes):
    copied_dict = dict(d)
    copied_dict.update(changes)
    return copied_dict


def _to_xwwwformurlencoded_data(template) -> str:
    _logger = logging.getLogger(__name__)
    _logger.debug('Encoding %s', template)
    e = {}
    jsonschemavalidator.CJ_TEMPLATE_SCHEMA_VALIDATOR.validate(template)
    for e_ in template['template']['data']:
        if 'section' in e_:
            raise jsonschemavalidator.ValidationError('XWWWFormUrlEncoded does not support the section property')
        if e_['value'] is not None:
            e[e_['name']] = e_['value']
    result = urlencode(e, True)
    _logger.debug('Returning %s', result)
    return result


def _ordered(obj):
    if isinstance(obj, dict):
        def _ordered_one(k, v):
            if k == 'rel' and isinstance(v, str):
                return k, _ordered(' '.join(sorted(v.split() if v else [])))
            else:
                return k, _ordered(v)
        return sorted((_ordered_one(k, v) for k, v in obj.items()))
    if isinstance(obj, list):
        try:
            return sorted(_ordered(x) for x in obj)
        except TypeError as t:
            print('obj is {}'.format(obj))
            raise t
    else:
        return str(obj)
